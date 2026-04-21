from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

import jwt
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from prometheus_fastapi_instrumentator import Instrumentator
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from src.inference.service import IDSInferenceService
from src.utils.config import load_config
from src.utils.logging import configure_logging
from src.utils.schemas import (
    BatchPredictionRequest,
    BatchPredictionResponse,
    ModelInfoResponse,
    PredictionResponse,
    TokenResponse,
    TrafficRecord,
)

CONFIG = load_config("configs/default.yaml")
configure_logging(CONFIG["app"]["log_level"])

JWT_SECRET = os.getenv("IDS_JWT_SECRET", CONFIG["security"]["jwt_secret"])
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = CONFIG["security"]["token_expire_minutes"]

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Intrusion Detection Platform", version="1.0.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

instrumentator = Instrumentator().instrument(app)
instrumentator.expose(app, endpoint="/metrics")

security_scheme = HTTPBearer()
service = IDSInferenceService(
    artifact_path=Path(CONFIG["paths"]["artifacts_dir"]) / "model_bundle.joblib",
    drift_threshold=CONFIG["monitoring"]["drift_threshold"],
)


def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)) -> str:
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return str(payload["sub"])
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "model": "loaded" if service.artifacts is not None else "fallback_mode"}


@app.get("/model_info", response_model=ModelInfoResponse)
def model_info(_: str = Depends(verify_token)) -> ModelInfoResponse:
    return ModelInfoResponse(**service.get_model_info())


@app.post("/token", response_model=TokenResponse)
def issue_token(username: str = "security-analyst") -> TokenResponse:
    return TokenResponse(access_token=create_access_token(username))


@app.post("/predict", response_model=PredictionResponse)
@limiter.limit(CONFIG["security"]["rate_limit"])
def predict(request: Request, record: TrafficRecord, _: str = Depends(verify_token)) -> PredictionResponse:
    result = service.predict_records([record.model_dump()])[0]
    return PredictionResponse(**result)


@app.post("/batch_predict", response_model=BatchPredictionResponse)
@limiter.limit(CONFIG["security"]["rate_limit"])
def batch_predict(request: Request, payload: BatchPredictionRequest, _: str = Depends(verify_token)) -> BatchPredictionResponse:
    results = service.predict_records([record.model_dump() for record in payload.records])
    return BatchPredictionResponse(predictions=[PredictionResponse(**item) for item in results])
