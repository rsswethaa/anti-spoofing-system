import unittest
import app as app_module
class EndToEndSmokeTests(unittest.TestCase):
    def setUp(self): app_module.app.config['TESTING']=True; self.client=app_module.app.test_client()
    def test_health_home_platform(self):
        self.assertEqual(self.client.get('/health').status_code,200); self.assertEqual(self.client.get('/').status_code,200); self.assertEqual(self.client.get('/api/platform/status').status_code,200)
    def test_pad_metrics(self):
        r=self.client.post('/api/benchmark',json={'bona_fide_scores':[.9,.8,.85],'attack_scores':[.1,.2,.3],'threshold':.5}); self.assertEqual(r.status_code,200); self.assertEqual(r.get_json()['metrics']['ACER'],0.0)
if __name__=='__main__': unittest.main()
