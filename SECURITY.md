# Security Boundary

## Status

TrueFace is a research/portfolio presentation-attack-detection prototype. It is **not** a certified biometric authentication control and should not protect real accounts or high-value actions.

## Threats considered in the prototype

- printed-photo presentation
- replay from a phone or display
- challenge replay
- low-quality mask/depth inconsistency signals
- synthetic frame injection as a production concern
- model probing and threshold gaming as production concerns

## Current controls

The prototype combines active challenge-response with several observable signals and stores the decision inputs for auditability. It also includes an optional CNN research path and APCER/BPCER/ACER evaluation utilities.

These controls do not establish standards compliance or resistance to sophisticated attacks.

## Privacy

Face images and biometric-derived signals are sensitive data. The public demo should be used only with consent and should not be treated as a production identity system. Real deployments would need strict purpose limitation, retention/deletion controls, encryption, access control and jurisdiction-specific biometric/privacy review.

## Production requirements

A real PAD/authentication system would additionally require:

- trusted capture and anti-injection/device attestation
- secure transport and protected model execution
- subject-disjoint and cross-dataset evaluation
- representative print/replay/mask/deepfake attacks
- calibrated operating thresholds
- independent penetration/security testing
- rate limiting and anti-automation controls
- model/version governance
- fallback/recovery procedures
- compliance review against the relevant biometric/PAD standards

## Vulnerability reporting

Do not publish exploitable bypass details or real biometric data in a public issue. Contact the repository owner privately through the GitHub profile with the affected version and reproduction steps.
