from flask import Blueprint, jsonify, request
from .pad_metrics import pad_metrics, threshold_sweep
def register_advanced(app):
    bp=Blueprint('trueface_advanced',__name__)
    @bp.post('/api/benchmark')
    def benchmark():
        p=request.get_json(silent=True) or {}
        try:
            metrics=pad_metrics(p.get('bona_fide_scores') or [],p.get('attack_scores') or [],p.get('threshold',.5)); sweep=threshold_sweep(p.get('bona_fide_scores') or [],p.get('attack_scores') or [],int(p.get('steps',21)))
        except (ValueError,TypeError,ZeroDivisionError) as exc: return jsonify({'error':str(exc)}),400
        return jsonify({'metrics':metrics,'threshold_sweep':sweep,'note':'Metrics are meaningful only for a documented representative PAD evaluation dataset.'})
    app.register_blueprint(bp)
