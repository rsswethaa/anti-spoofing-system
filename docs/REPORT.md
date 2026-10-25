# Technical Project Report — Anti-Spoofing System

## Executive summary
This project models a complete presentation-attack detection workflow: liveness signal extraction, challenge evidence, score fusion, thresholded decision, durable audit storage and security-focused documentation.

## 1. Problem
Face authentication can be attacked using printed photos, screens, replay video, masks or injected synthetic inputs.

## 2. Objective
Demonstrate a multi-signal liveness architecture that is explainable, testable and auditable rather than depending on one opaque score.

## 3. Method
The baseline fuses normalised texture, motion, depth-consistency and challenge-response signals using explicit weights and a configurable threshold.

## 4. Persistence/audit design
Each liveness session stores raw evidence summaries, active challenges and exactly one final decision with the model version and threshold used. This supports incident review and reproducibility.

## 5. Testing
Synthetic tests verify expected genuine/spoof ordering and invalid inputs. Storage tests validate complete evidence-to-decision persistence. CI compiles and runs all tests.

## 6. Security model
Real deployment must assume active adversaries. Secure sensor paths, anti-replay challenges, authenticated sessions, tamper-resistant logs and fallback policy are as important as the classifier itself.

## 7. Limitations
No production biometric assurance, certified PAD metrics, real attack dataset or device-specific robustness is claimed.

## 8. Future work
CNN/ViT models, optical flow, depth cameras, challenge randomisation, cross-dataset tests, standard PAD metrics and adversarial security review.

## Conclusion
The repository includes working scoring logic, a real audit database, SQL assets, diagrams, tests, CI, security/threat documentation, a model card and full technical report.
