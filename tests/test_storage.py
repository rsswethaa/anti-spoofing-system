import sqlite3
import tempfile
import unittest
from pathlib import Path

from src.storage import add_challenge, add_observation, create_session, init_db, save_decision


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = Path(self.tmp.name) / 'antispoof.db'
        init_db(self.db)

    def tearDown(self):
        self.tmp.cleanup()

    def test_complete_liveness_audit(self):
        session = create_session(self.db, 'SESSION-1', 'camera-A')
        add_observation(self.db, session, 0.9, 0.8, 0.85)
        add_challenge(self.db, session, 'blink', True)
        save_decision(self.db, session, 'GENUINE', 0.86, 0.6, 'Strong multi-signal liveness evidence')
        with sqlite3.connect(self.db) as db:
            self.assertEqual(db.execute('SELECT label FROM liveness_decisions').fetchone()[0], 'GENUINE')
            self.assertEqual(db.execute('SELECT status FROM liveness_sessions WHERE id=?',(session,)).fetchone()[0], 'DECIDED')


if __name__ == '__main__':
    unittest.main()
