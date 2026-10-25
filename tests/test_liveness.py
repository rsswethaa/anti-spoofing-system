import unittest
from src.liveness import LivenessSignals, classify, liveness_score

class LivenessTests(unittest.TestCase):
    def test_live_scores_above_spoof(self):
        live = LivenessSignals(0.9,0.8,0.85,0.9)
        spoof = LivenessSignals(0.2,0.3,0.2,0.1)
        self.assertGreater(liveness_score(live), liveness_score(spoof))

    def test_classification(self):
        live = LivenessSignals(0.9,0.8,0.85,0.9)
        self.assertEqual(classify(live)["label"], "GENUINE")

    def test_invalid_signal(self):
        with self.assertRaises(ValueError):
            classify(LivenessSignals(1.2,0.5,0.5,0.5))

if __name__ == "__main__":
    unittest.main()
