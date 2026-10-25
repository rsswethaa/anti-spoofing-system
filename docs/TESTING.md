# Testing Strategy

Automated tests cover liveness feature validation, expected ordering of genuine/spoof-like synthetic profiles, threshold behaviour and complete SQLite evidence/decision persistence.

Run:
```bash
python -m unittest discover -s tests -v
```

Production PAD testing would require representative devices and attacks, cross-dataset evaluation, replay/print/mask variations, environmental conditions and standard PAD metrics such as APCER/BPCER with confidence intervals.
