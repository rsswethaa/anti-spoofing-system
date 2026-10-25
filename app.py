import os
from pathlib import Path
from uuid import uuid4

from flask import Flask, jsonify, render_template, request

from src.live_session import LiveLivenessSession
from src.storage import add_challenge, add_observation, create_session, init_db, save_decision

app = Flask(__name__)
app.config['DATABASE'] = os.getenv('LIVENESS_DB', str(Path('instance') / 'liveness.db'))
SESSIONS = {}


def ensure_db():
    db_path = Path(app.config['DATABASE'])
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if not db_path.exists():
        init_db(db_path)
    return db_path


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/health')
def health():
    return jsonify({'status':'ok','service':'live-anti-spoofing'})


@app.post('/api/session')
def start_session():
    payload = request.get_json(silent=True) or {}
    challenge = payload.get('challenge', 'BLINK_TWICE')
    try:
        engine = LiveLivenessSession(challenge=challenge)
    except ValueError as exc:
        return jsonify({'error':str(exc)}), 400
    ref = uuid4().hex[:16]
    db_id = create_session(ensure_db(), ref, payload.get('device_ref','browser-demo'))
    SESSIONS[ref] = {'engine':engine,'db_id':db_id,'saved':False}
    instruction = 'Blink twice naturally' if challenge == 'BLINK_TWICE' else 'Turn your head gently to one side'
    return jsonify({'session_ref':ref,'challenge':challenge,'instruction':instruction})


@app.post('/api/session/<ref>/frame')
def frame(ref):
    session = SESSIONS.get(ref)
    if not session:
        return jsonify({'error':'unknown session'}), 404
    payload = request.get_json(silent=True) or {}
    try:
        result = session['engine'].process(payload.get('landmarks') or [], payload.get('texture_score', .7))
    except (TypeError, ValueError) as exc:
        return jsonify({'error':str(exc)}), 400
    add_observation(ensure_db(), session['db_id'], result['texture_score'], result['motion_score'], result['depth_consistency'])
    if result['decision'] and not session['saved']:
        passed = result['challenge_complete']
        add_challenge(ensure_db(), session['db_id'], result['challenge'], passed)
        d = result['decision']
        db_label = 'GENUINE' if d['label'] == 'GENUINE' else 'SPOOF'
        save_decision(ensure_db(), session['db_id'], db_label, d['liveness_score'], d['threshold'], explanation='Live multi-signal portfolio prototype')
        session['saved'] = True
    return jsonify(result)


if __name__ == '__main__':
    ensure_db()
    app.run(debug=True)
