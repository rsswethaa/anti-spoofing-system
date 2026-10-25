# Interface Contracts

Core anti-spoof scoring interfaces live under `src/` and are demonstrated by `demo.py`.

Persistence interfaces:
- `init_db(path, seed=False)`
- `create_session(path, session_ref, device_ref)`
- `add_observation(path, session_id, texture, motion, depth)`
- `add_challenge(path, session_id, challenge_type, passed)`
- `save_decision(path, session_id, label, score, threshold, explanation, model_version)`

A production biometric gateway would wrap these calls behind authenticated device/session APIs and signed sensor provenance.
