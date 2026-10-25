from collections import defaultdict


def evaluate_pad(records, threshold=0.5):
    """Calculate presentation-attack metrics from liveness scores.

    records: iterable of {label: 'BONA_FIDE'|'ATTACK', score: 0..1,
                          attack_type: optional string}
    score >= threshold is accepted as bona fide.
    """
    bona_total = bona_rejected = 0
    attack_totals = defaultdict(int)
    attack_accepted = defaultdict(int)
    for row in records:
        label = str(row['label']).upper()
        score = float(row['score'])
        if not 0 <= score <= 1:
            raise ValueError('score must be between 0 and 1')
        accepted = score >= threshold
        if label == 'BONA_FIDE':
            bona_total += 1
            bona_rejected += int(not accepted)
        elif label == 'ATTACK':
            attack_type = str(row.get('attack_type') or 'UNSPECIFIED').upper()
            attack_totals[attack_type] += 1
            attack_accepted[attack_type] += int(accepted)
        else:
            raise ValueError('label must be BONA_FIDE or ATTACK')
    bpcer = bona_rejected / bona_total if bona_total else None
    apcer_by_type = {
        attack: attack_accepted[attack] / total
        for attack, total in sorted(attack_totals.items())
    }
    attack_total = sum(attack_totals.values())
    overall_apcer = sum(attack_accepted.values()) / attack_total if attack_total else None
    acer = (overall_apcer + bpcer) / 2 if overall_apcer is not None and bpcer is not None else None
    return {
        'threshold': threshold,
        'bona_fide_count': bona_total,
        'attack_count': attack_total,
        'bpcer': None if bpcer is None else round(bpcer, 6),
        'apcer': None if overall_apcer is None else round(overall_apcer, 6),
        'apcer_by_attack_type': {k: round(v, 6) for k, v in apcer_by_type.items()},
        'acer': None if acer is None else round(acer, 6),
    }
