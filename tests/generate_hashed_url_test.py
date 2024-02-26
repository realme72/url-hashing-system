import unittest
from routes.routes import app

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_generate_hashed_url(self):
        # Test valid request
        response = self.app.post('/generate', json={'url': 'https://example.com'})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('hashed_url', data)

        # Test missing URL in request body
        response = self.app.post('/generate', json={})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()
