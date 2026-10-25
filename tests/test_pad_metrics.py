import unittest

from src.pad_metrics import evaluate_pad


class PadMetricTests(unittest.TestCase):
    def test_apcer_bpcer_by_attack_type(self):
        rows = [
            {'label':'BONA_FIDE','score':.9},
            {'label':'BONA_FIDE','score':.4},
            {'label':'ATTACK','attack_type':'PRINT','score':.7},
            {'label':'ATTACK','attack_type':'PRINT','score':.2},
            {'label':'ATTACK','attack_type':'REPLAY','score':.1},
            {'label':'ATTACK','attack_type':'MASK','score':.8},
        ]
        result = evaluate_pad(rows, threshold=.5)
        self.assertEqual(result['bpcer'], .5)
        self.assertEqual(result['apcer_by_attack_type']['PRINT'], .5)
        self.assertEqual(result['apcer_by_attack_type']['REPLAY'], 0.0)
        self.assertEqual(result['apcer_by_attack_type']['MASK'], 1.0)
        self.assertEqual(result['attack_count'], 4)

    def test_invalid_score_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_pad([{'label':'ATTACK','score':1.2,'attack_type':'PRINT'}])


if __name__ == '__main__':
    unittest.main()
