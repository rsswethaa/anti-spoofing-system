def pad_metrics(bona_fide_scores, attack_scores, threshold=.5):
    bona = [float(x) for x in bona_fide_scores]
    attacks = [float(x) for x in attack_scores]
    if not bona or not attacks:
        raise ValueError('bona_fide_scores and attack_scores are required')
    threshold = float(threshold)
    if not 0 <= threshold <= 1:
        raise ValueError('threshold must be between 0 and 1')
    if any(not 0 <= s <= 1 for s in bona + attacks):
        raise ValueError('scores must be between 0 and 1')
    bpcer = sum(s < threshold for s in bona) / len(bona)
    apcer = sum(s >= threshold for s in attacks) / len(attacks)
    acer = (bpcer + apcer) / 2
    return {
        'threshold': round(threshold, 4),
        'APCER': round(apcer, 4),
        'BPCER': round(bpcer, 4),
        'ACER': round(acer, 4),
        'bona_fide_samples': len(bona),
        'attack_samples': len(attacks),
    }


def evaluate_pad(rows, threshold=.5):
    """Backwards-compatible PAD evaluation with attack-type APCER breakdown."""
    threshold = float(threshold)
    if not 0 <= threshold <= 1:
        raise ValueError('threshold must be between 0 and 1')
    bona = []
    attacks = []
    by_type = {}
    for row in rows:
        score = float(row.get('score'))
        if not 0 <= score <= 1:
            raise ValueError('scores must be between 0 and 1')
        label = str(row.get('label', '')).upper()
        if label == 'BONA_FIDE':
            bona.append(score)
        elif label == 'ATTACK':
            attacks.append(score)
            attack_type = str(row.get('attack_type') or 'UNKNOWN').upper()
            by_type.setdefault(attack_type, []).append(score)
        else:
            raise ValueError('label must be BONA_FIDE or ATTACK')
    if not bona or not attacks:
        raise ValueError('at least one bona-fide and one attack sample are required')
    bpcer = sum(s < threshold for s in bona) / len(bona)
    apcer_by_type = {
        name: round(sum(s >= threshold for s in values) / len(values), 4)
        for name, values in by_type.items()
    }
    overall_apcer = sum(s >= threshold for s in attacks) / len(attacks)
    return {
        'threshold': round(threshold, 4),
        'bpcer': round(bpcer, 4),
        'apcer': round(overall_apcer, 4),
        'acer': round((bpcer + overall_apcer) / 2, 4),
        'apcer_by_attack_type': apcer_by_type,
        'bona_fide_count': len(bona),
        'attack_count': len(attacks),
    }


def threshold_sweep(bona, attacks, steps=21):
    if int(steps) < 2:
        raise ValueError('steps must be at least 2')
    rows = [pad_metrics(bona, attacks, i / (int(steps) - 1)) for i in range(int(steps))]
    best = min(rows, key=lambda r: (r['ACER'], abs(r['APCER'] - r['BPCER'])))
    return {'best_by_acer': best, 'curve': rows}
