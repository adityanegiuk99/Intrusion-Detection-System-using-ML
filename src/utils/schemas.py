from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class TrafficRecord(BaseModel):
    duration: float = Field(ge=0)
    protocol_type: str
    service: str
    flag: str
    src_bytes: float = Field(ge=0)
    dst_bytes: float = Field(ge=0)
    land: int = Field(ge=0, le=1)
    wrong_fragment: float = Field(ge=0)
    urgent: float = Field(ge=0)
    hot: float = Field(ge=0)
    num_failed_logins: float = Field(ge=0)
    logged_in: int = Field(ge=0, le=1)
    num_compromised: float = Field(ge=0)
    root_shell: int = Field(ge=0, le=1)
    su_attempted: float = Field(ge=0)
    num_root: float = Field(ge=0)
    num_file_creations: float = Field(ge=0)
    num_shells: float = Field(ge=0)
    num_access_files: float = Field(ge=0)
    num_outbound_cmds: float = Field(ge=0)
    is_host_login: int = Field(ge=0, le=1)
    is_guest_login: int = Field(ge=0, le=1)
    count: float = Field(ge=0)
    srv_count: float = Field(ge=0)
    serror_rate: float = Field(ge=0)
    srv_serror_rate: float = Field(ge=0)
    rerror_rate: float = Field(ge=0)
    srv_rerror_rate: float = Field(ge=0)
    same_srv_rate: float = Field(ge=0)
    diff_srv_rate: float = Field(ge=0)
    srv_diff_host_rate: float = Field(ge=0)
    dst_host_count: float = Field(ge=0)
    dst_host_srv_count: float = Field(ge=0)
    dst_host_same_srv_rate: float = Field(ge=0)
    dst_host_diff_srv_rate: float = Field(ge=0)
    dst_host_same_src_port_rate: float = Field(ge=0)
    dst_host_srv_diff_host_rate: float = Field(ge=0)
    dst_host_serror_rate: float = Field(ge=0)
    dst_host_srv_serror_rate: float = Field(ge=0)
    dst_host_rerror_rate: float = Field(ge=0)
    dst_host_srv_rerror_rate: float = Field(ge=0)


class BatchPredictionRequest(BaseModel):
    records: list[TrafficRecord]


class PredictionResponse(BaseModel):
    prediction: str
    label_id: int
    probability: float
    drift_score: float
    drift_detected: bool
    top_features: list[dict[str, Any]]


class BatchPredictionResponse(BaseModel):
    predictions: list[PredictionResponse]


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

