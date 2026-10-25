from dataclasses import dataclass

@dataclass
class LivenessSignals:
    texture_score: float
    motion_score: float
    depth_consistency: float
    challenge_response: float


def validate(signals: LivenessSignals) -> None:
    for name, value in signals.__dict__.items():
        if not 0 <= value <= 1:
            raise ValueError(f"{name} must be between 0 and 1")


def liveness_score(signals: LivenessSignals) -> float:
    validate(signals)
    score = (
        0.30 * signals.texture_score
        + 0.25 * signals.motion_score
        + 0.25 * signals.depth_consistency
        + 0.20 * signals.challenge_response
    )
    return round(score, 4)


def classify(signals: LivenessSignals, threshold: float = 0.62) -> dict:
    if not 0 < threshold < 1:
        raise ValueError("threshold must be between 0 and 1")
    score = liveness_score(signals)
    label = "GENUINE" if score >= threshold else "SPOOF_SUSPECTED"
    return {"label": label, "liveness_score": score, "threshold": threshold}
