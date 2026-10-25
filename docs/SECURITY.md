# Security and Threat Model

Anti-spoofing is itself a security control and must be treated as adversarially exposed.

## Threats
Printed photos, replayed screens/video, masks, injection of synthetic frames, sensor bypass, challenge replay and model probing.

## Production controls
Secure camera path, device attestation where available, nonce-based/randomised challenges, TLS, authenticated sessions, rate limiting, tamper-resistant logs, secrets management and monitored fallback policy.

## Privacy
Biometric imagery/templates are highly sensitive. Minimise collection and retention, restrict access and follow applicable biometric/privacy law.
