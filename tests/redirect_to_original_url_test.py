import unittest
from routes.routes import app

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_redirect_to_original_url(self):
        # Mock URL_MAP for testing
        app.config['URL_MAP'] = {'abcdef': {'original_url': 'https://example.com'}}

        # Test valid hashed URL
        response = self.app.get('/abcdef')
        self.assertEqual(response.status_code, 302)
        data = response.get_json()
        self.assertIn('original_url', data)

        # Test invalid hashed URL
        response = self.app.get('/invalid_hash')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()
