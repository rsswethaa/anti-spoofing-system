from src.liveness import LivenessSignals, classify
from src.explanation import explain

live = LivenessSignals(0.82, 0.76, 0.79, 0.90)
spoof = LivenessSignals(0.30, 0.25, 0.20, 0.10)
print("Live sample:", classify(live), explain(live))
print("Spoof sample:", classify(spoof), explain(spoof))
