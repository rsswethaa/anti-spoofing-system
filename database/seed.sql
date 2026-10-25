INSERT OR IGNORE INTO liveness_sessions(session_ref, device_ref, status) VALUES
('SYNTH-GENUINE-001','demo-device','OPEN'),
('SYNTH-SPOOF-001','demo-device','OPEN');

INSERT INTO signal_observations(session_id, texture_score, motion_score, depth_score)
SELECT id, 0.91, 0.86, 0.88 FROM liveness_sessions WHERE session_ref='SYNTH-GENUINE-001'
AND NOT EXISTS (SELECT 1 FROM signal_observations s JOIN liveness_sessions l ON l.id=s.session_id WHERE l.session_ref='SYNTH-GENUINE-001');

INSERT INTO signal_observations(session_id, texture_score, motion_score, depth_score)
SELECT id, 0.25, 0.18, 0.20 FROM liveness_sessions WHERE session_ref='SYNTH-SPOOF-001'
AND NOT EXISTS (SELECT 1 FROM signal_observations s JOIN liveness_sessions l ON l.id=s.session_id WHERE l.session_ref='SYNTH-SPOOF-001');
