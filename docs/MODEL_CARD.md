# Model Card — Fusion Baseline v1

## Intended use
Educational presentation-attack detection demonstration using multiple liveness signals.

## Inputs
Normalised texture, motion, depth-consistency and challenge-response evidence.

## Output
Genuine/spoof label plus score relative to a configured threshold.

## Limitations
Synthetic tests do not represent real attack diversity. Scores are not calibrated probabilities. No APCER/BPCER, FAR/FRR or certification claim is made.

## Prohibited use
Do not treat this repository as sufficient protection for financial, identity, border, healthcare or other high-assurance authentication systems.
