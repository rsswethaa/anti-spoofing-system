import os
from pathlib import Path
from uuid import uuid4
from flask import Flask, jsonify, render_template, request
from src.live_session import LiveLivenessSession
from src.storage import add_challenge, add_observation, create_session, init_db, save_decision
app=Flask(__name__); app.config['DATABASE']=os.getenv('LIVENESS_DB',str(Path('instance')/'liveness.db')); app.config['CNN_MODEL']=os.getenv('CNN_MODEL','models/anti_spoof_cnn.pt'); SESSIONS={}
def ensure_db():
    db_path=Path(app.config['DATABASE']); db_path.parent.mkdir(parents=True,exist_ok=True)
    if not db_path.exists(): init_db(db_path)
    return db_path
@app.get('/')
def index(): return render_template('index.html')
@app.get('/health')
def health(): return jsonify({'status':'ok','service':'live-anti-spoofing','cnn_model_available':Path(app.config['CNN_MODEL']).exists()})
@app.post('/api/session')
def start_session():
    p=request.get_json(silent=True) or {}; challenge=p.get('challenge','BLINK_TWICE')
    try: engine=LiveLivenessSession(challenge=challenge)
    except ValueError as exc: return jsonify({'error':str(exc)}),400
    ref=uuid4().hex[:16]; db_id=create_session(ensure_db(),ref,p.get('device_ref','browser-demo')); SESSIONS[ref]={'engine':engine,'db_id':db_id,'saved':False}; instruction='Blink twice naturally' if challenge=='BLINK_TWICE' else 'Turn your head gently to one side'; return jsonify({'session_ref':ref,'challenge':challenge,'instruction':instruction})
@app.post('/api/session/<ref>/frame')
def frame(ref):
    session=SESSIONS.get(ref)
    if not session: return jsonify({'error':'unknown session'}),404
    p=request.get_json(silent=True) or {}
    try: result=session['engine'].process(p.get('landmarks') or [],p.get('texture_score',.7))
    except (TypeError,ValueError) as exc: return jsonify({'error':str(exc)}),400
    add_observation(ensure_db(),session['db_id'],result['texture_score'],result['motion_score'],result['depth_consistency'])
    if result['decision'] and not session['saved']:
        passed=result['challenge_complete']; add_challenge(ensure_db(),session['db_id'],result['challenge'],passed); d=result['decision']; db_label='GENUINE' if d['label']=='GENUINE' else 'SPOOF'; save_decision(ensure_db(),session['db_id'],db_label,d['liveness_score'],d['threshold'],explanation='Live multi-signal portfolio prototype'); session['saved']=True
    return jsonify(result)
@app.post('/api/cnn/score')
def cnn_score():
    image=request.files.get('image')
    if not image or not image.filename: return jsonify({'error':'image is required'}),400
    if not Path(app.config['CNN_MODEL']).exists(): return jsonify({'error':'CNN model is not trained/installed','hint':'See research/train_cnn.py and requirements-cnn.txt'}),503
    try:
        from src.cnn_liveness import score_image_bytes
        score=score_image_bytes(image.read(),app.config['CNN_MODEL'])
    except (RuntimeError,FileNotFoundError) as exc: return jsonify({'error':str(exc)}),503
    except Exception as exc: return jsonify({'error':f'CNN scoring failed: {exc}'}),400
    return jsonify({'bona_fide_probability':round(score,6),'attack_probability':round(1-score,6),'model':Path(app.config['CNN_MODEL']).name})
from src.advanced import register_advanced
from src.platform import init_platform
register_advanced(app); init_platform(app,'trueface')
if __name__=='__main__': ensure_db(); app.run(host='0.0.0.0',port=int(os.getenv('PORT','5000')),debug=os.getenv('FLASK_DEBUG')=='1')
