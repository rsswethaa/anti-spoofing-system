from .liveness import LivenessSignals

def explain(signals: LivenessSignals) -> list[str]:
    reasons = []
    if signals.texture_score < 0.5:
        reasons.append("Low texture-liveness signal; printed/screen presentation should be reviewed.")
    if signals.motion_score < 0.5:
        reasons.append("Limited natural facial motion detected.")
    if signals.depth_consistency < 0.5:
        reasons.append("Depth consistency is weak for a live 3D face.")
    if signals.challenge_response < 0.5:
        reasons.append("Challenge-response evidence is insufficient.")
    return reasons or ["All demonstration liveness signals are above the review threshold."]
