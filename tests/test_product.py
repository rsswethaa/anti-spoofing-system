import tempfile
import unittest
from pathlib import Path

import app as live_app
from src.live_session import LiveLivenessSession, face_features


def face(open_eye=True,nose=.5,width=.4):
    p=[[.5,.5] for _ in range(468)]
    p[234]=[.5-width/2,.5];p[454]=[.5+width/2,.5];p[1]=[nose,.46]
    p[33]=[.40,.50];p[133]=[.46,.50];p[362]=[.54,.50];p[263]=[.60,.50]
    if open_eye:
        p[159]=[.43,.47];p[145]=[.43,.53];p[386]=[.57,.47];p[374]=[.57,.53]
    else:
        p[159]=[.43,.499];p[145]=[.43,.501];p[386]=[.57,.499];p[374]=[.57,.501]
    return p


class ProductTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();live_app.app.config.update(TESTING=True,DATABASE=str(Path(self.tmp.name)/'test.db'));live_app.SESSIONS.clear();self.client=live_app.app.test_client()
    def tearDown(self):self.tmp.cleanup()

    def test_face_features_detect_eye_closure(self):
        self.assertGreater(face_features(face(True))['eye_ratio'], face_features(face(False))['eye_ratio'])

    def test_two_blink_challenge_completes(self):
        s=LiveLivenessSession('BLINK_TWICE')
        result=None
        for frame in [face(True),face(False),face(True),face(False),face(True),face(True)]:
            result=s.process(frame,.85)
        self.assertEqual(result['blink_count'],2);self.assertTrue(result['challenge_complete']);self.assertIsNotNone(result['decision'])

    def test_turn_challenge_completes(self):
        s=LiveLivenessSession('TURN_SIDE')
        result=None
        for x in [.50,.52,.55,.58,.60,.62]:result=s.process(face(True,nose=x),.8)
        self.assertTrue(result['challenge_complete']);self.assertIsNotNone(result['decision'])

    def test_end_to_end_api_persists_decision(self):
        start=self.client.post('/api/session',json={'challenge':'BLINK_TWICE'}).get_json();ref=start['session_ref'];last=None
        for f in [face(True),face(False),face(True),face(False),face(True),face(True)]:
            last=self.client.post(f'/api/session/{ref}/frame',json={'landmarks':f,'texture_score':.9})
        self.assertEqual(last.status_code,200);self.assertIsNotNone(last.get_json()['decision'])

    def test_rejects_unknown_session(self):
        self.assertEqual(self.client.post('/api/session/nope/frame',json={}).status_code,404)


if __name__=='__main__':unittest.main()
