# Architecture

```mermaid
sequenceDiagram
  participant C as Camera
  participant D as Face Detector
  participant X as Feature Extractors
  participant M as Anti-Spoof Model
  participant A as Access Layer
  C->>D: frame sequence
  D-->>X: aligned face region
  X-->>M: texture + motion + depth + challenge signals
  M-->>A: liveness score + decision
```

The reference implementation keeps feature fusion transparent and deterministic. A full DL research system could use CNN/Transformer-based presentation-attack detection trained on consented datasets and evaluated across print, replay, mask and adversarial conditions.
