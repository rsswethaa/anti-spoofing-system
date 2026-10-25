# Presentation-Attack Evaluation

The live TrueFace demo combines FaceMesh geometry, blink/head-turn challenges, texture and motion signals. A separate research path is provided for evaluating a trained CNN on bona-fide and presentation-attack data.

## Attack classes
A serious evaluation should include attack categories such as:

- printed photograph;
- phone/tablet replay;
- prerecorded video replay;
- partial or full mask;
- where possible, injection or virtual-camera attacks as a separate threat class.

## Metrics
`src/pad_metrics.py` reports:

- **APCER** — proportion of attack presentations incorrectly accepted as bona fide;
- **BPCER** — proportion of bona-fide presentations incorrectly rejected;
- APCER by attack type;
- **ACER** — arithmetic mean of APCER and BPCER for a selected threshold.

These metrics are threshold-dependent. Report the threshold and the evaluation protocol with every result.

## CNN research path
Install optional dependencies:

```bash
pip install -r requirements-cnn.txt
```

Expected training structure:

```text
dataset/
  train/
    bona_fide/
    print/
    replay/
    mask/
  val/
    bona_fide/
    print/
    replay/
    mask/
```

Train:

```bash
python research/train_cnn.py dataset --epochs 10
```

The generated model is stored at `models/anti_spoof_cnn.pt` by default. The Flask product then exposes `POST /api/cnn/score` for optional face-image scoring.

## Evaluate PAD scores
Create a CSV with:

```text
label,score,attack_type
BONA_FIDE,0.93,
ATTACK,0.18,PRINT
ATTACK,0.25,REPLAY
```

Then run:

```bash
python research/evaluate_pad.py predictions.csv --threshold 0.5
```

## Dataset integrity
Do not present metrics from synthetic examples as biometric-security performance. A defensible benchmark requires a documented public or permissioned PAD dataset, subject-disjoint splits, device/protocol details, attack-type coverage and ideally cross-dataset testing.

## Security boundary
A CNN score alone is not enough for production authentication. Production PAD also needs secure capture, anti-injection controls, device integrity, challenge randomisation, monitoring, privacy controls and independent security evaluation.
