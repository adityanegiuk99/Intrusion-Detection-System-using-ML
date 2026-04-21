from fastapi.testclient import TestClient

from api.main import app, create_access_token


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_predict_requires_auth():
    payload = {
        "duration": 1,
        "protocol_type": "tcp",
        "service": "http",
        "flag": "SF",
        "src_bytes": 120,
        "dst_bytes": 60,
        "land": 0,
        "wrong_fragment": 0,
        "urgent": 0,
        "hot": 0,
        "num_failed_logins": 0,
        "logged_in": 1,
        "num_compromised": 0,
        "root_shell": 0,
        "su_attempted": 0,
        "num_root": 0,
        "num_file_creations": 0,
        "num_shells": 0,
        "num_access_files": 0,
        "num_outbound_cmds": 0,
        "is_host_login": 0,
        "is_guest_login": 0,
        "count": 1,
        "srv_count": 1,
        "serror_rate": 0,
        "srv_serror_rate": 0,
        "rerror_rate": 0,
        "srv_rerror_rate": 0,
        "same_srv_rate": 1,
        "diff_srv_rate": 0,
        "srv_diff_host_rate": 0,
        "dst_host_count": 2,
        "dst_host_srv_count": 2,
        "dst_host_same_srv_rate": 1,
        "dst_host_diff_srv_rate": 0,
        "dst_host_same_src_port_rate": 0.1,
        "dst_host_srv_diff_host_rate": 0,
        "dst_host_serror_rate": 0,
        "dst_host_srv_serror_rate": 0,
        "dst_host_rerror_rate": 0,
        "dst_host_srv_rerror_rate": 0,
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 403


def test_token_generation():
    token = create_access_token("tester")
    assert isinstance(token, str)


def test_model_info_endpoint_requires_auth_and_returns_state():
    unauthorized = client.get("/model_info")
    assert unauthorized.status_code == 403

    token = create_access_token("tester")
    authorized = client.get("/model_info", headers={"Authorization": f"Bearer {token}"})
    assert authorized.status_code == 200
    payload = authorized.json()
    assert "artifact_loaded" in payload
    assert "status" in payload
