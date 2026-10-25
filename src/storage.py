from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / 'database' / 'schema.sql'
SEED = ROOT / 'database' / 'seed.sql'


def connect(db_path):
    db = sqlite3.connect(db_path)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA foreign_keys = ON')
    return db


def init_db(db_path, seed=False):
    with connect(db_path) as db:
        db.executescript(SCHEMA.read_text(encoding='utf-8'))
        if seed:
            db.executescript(SEED.read_text(encoding='utf-8'))
    return Path(db_path)


def create_session(db_path, session_ref, device_ref=''):
    with connect(db_path) as db:
        cur = db.execute('INSERT INTO liveness_sessions(session_ref,device_ref) VALUES (?,?)', (session_ref, device_ref))
        return cur.lastrowid


def add_observation(db_path, session_id, texture, motion, depth):
    with connect(db_path) as db:
        db.execute('INSERT INTO signal_observations(session_id,texture_score,motion_score,depth_score) VALUES (?,?,?,?)',
                   (session_id, float(texture), float(motion), float(depth)))


def add_challenge(db_path, session_id, challenge_type, passed):
    with connect(db_path) as db:
        db.execute('INSERT INTO challenge_events(session_id,challenge_type,passed) VALUES (?,?,?)',
                   (session_id, challenge_type, int(bool(passed))))


def save_decision(db_path, session_id, label, score, threshold, explanation='', model_version='fusion-baseline-v1'):
    with connect(db_path) as db:
        db.execute('''INSERT INTO liveness_decisions(session_id,label,score,threshold,model_version,explanation)
                      VALUES (?,?,?,?,?,?)''',
                   (session_id, label, float(score), float(threshold), model_version, explanation))
        db.execute("UPDATE liveness_sessions SET status='DECIDED' WHERE id=?", (session_id,))
