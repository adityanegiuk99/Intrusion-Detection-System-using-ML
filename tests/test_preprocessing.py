from src.preprocessing.pipeline import add_engineered_features, prepare_inference_frame


def test_engineered_features_are_created():
    frame = prepare_inference_frame(
        [
            {
                "duration": 1,
                "protocol_type": "tcp",
                "service": "http",
                "flag": "SF",
                "src_bytes": 100,
                "dst_bytes": 50,
                "land": 0,
                "wrong_fragment": 0,
                "urgent": 0,
                "hot": 1,
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
                "count": 2,
                "srv_count": 2,
                "serror_rate": 0.1,
                "srv_serror_rate": 0.1,
                "rerror_rate": 0.0,
                "srv_rerror_rate": 0.0,
                "same_srv_rate": 1.0,
                "diff_srv_rate": 0.0,
                "srv_diff_host_rate": 0.0,
                "dst_host_count": 5,
                "dst_host_srv_count": 5,
                "dst_host_same_srv_rate": 1.0,
                "dst_host_diff_srv_rate": 0.0,
                "dst_host_same_src_port_rate": 0.2,
                "dst_host_srv_diff_host_rate": 0.0,
                "dst_host_serror_rate": 0.0,
                "dst_host_srv_serror_rate": 0.0,
                "dst_host_rerror_rate": 0.0,
                "dst_host_srv_rerror_rate": 0.0,
            }
        ]
    )
    enriched = add_engineered_features(frame)
    assert "byte_ratio" in enriched.columns
    assert "privilege_escalation_risk" in enriched.columns

