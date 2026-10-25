-- Decision audit trail
SELECT s.session_ref, s.device_ref, d.label, d.score, d.threshold, d.model_version, d.created_at
FROM liveness_decisions d JOIN liveness_sessions s ON s.id=d.session_id
ORDER BY d.id DESC;

-- Evidence summary per session
SELECT s.session_ref,
       ROUND(AVG(o.texture_score),3) AS texture,
       ROUND(AVG(o.motion_score),3) AS motion,
       ROUND(AVG(o.depth_score),3) AS depth,
       SUM(CASE WHEN c.passed=1 THEN 1 ELSE 0 END) AS challenges_passed
FROM liveness_sessions s
LEFT JOIN signal_observations o ON o.session_id=s.id
LEFT JOIN challenge_events c ON c.session_id=s.id
GROUP BY s.id;
