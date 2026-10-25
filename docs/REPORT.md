# Technical Report

## Problem
Face authentication systems can be attacked with printed photos, screens, replayed video or masks. Anti-spoofing attempts to distinguish a live subject from a presentation attack.

## Objective
Demonstrate an explainable liveness pipeline that combines multiple evidence sources rather than relying on a single signal.

## Method
The portfolio baseline fuses normalised texture, motion, depth-consistency and challenge-response signals using explicit weights and a configurable threshold.

## Evaluation
Synthetic tests verify that strong liveness profiles score above spoof-like profiles, thresholding behaves predictably and invalid feature values are rejected.

## Security limitations
No production biometric assurance, FAR/FRR, APCER/BPCER or ISO-compliance claim is made. Real deployment requires representative attack datasets, device-specific testing, secure sensor paths, adversarial evaluation and continuous monitoring.

## Future work
CNN/ViT classifiers, optical-flow features, depth cameras, challenge randomisation, cross-dataset testing and calibrated presentation-attack metrics.
