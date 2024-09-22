import unittest
import json

from server.server import init_app
from server.model.form import Form
from server.model.form_encoder import FormEncoder

class TestServer(unittest.TestCase):

    def setUp(self):
        self.app = init_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code,200)
        self.assertIn(b'Home',response.data)

    def test_submit_files(self):
        form = Form(userid="userid",appid="blah",applanguage="java",configtext="other")
        response = self.client.post('/api/order',
                                    data=json.dumps(form,cls=FormEncoder),
                                    content_type='application/json')        
        self.assertEqual(response.status_code,200)


if __name__ == '__main__':
    unittest.main()