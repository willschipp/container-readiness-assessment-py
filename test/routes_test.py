import unittest
import json
from flask import Flask, jsonify
from flask.testing import FlaskClient
from server.handler.routes import main 
from server.model.form import Form
from server.model.form_encoder import FormEncoder

class TestSubmitFiles(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(main)
        self.client = self.app.test_client()

    def test_submit_files_success(self):
        # Test successful JSON submission
        form = Form(userid="hello",appid="1234",applanguage="java",configtext="blah")
        json_str = json.dumps(form,cls=FormEncoder)
        headers = {"Content-type":"application/json"}
        response = self.client.post('/api/order', data=json_str,headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("orderid",response.json)

    def test_submit_files_invalid_content_type(self):
        # Test submission with invalid content type
        test_data = "This is not JSON"
        response = self.client.post('/api/order', data=test_data, content_type='text/plain')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "parsing json"})

    def test_submit_files_empty_json(self):
        # Test submission with empty JSON
        response = self.client.post('/api/order', json={})
        self.assertEqual(response.status_code, 500)

if __name__ == '__main__':
    unittest.main()