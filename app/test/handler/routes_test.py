import unittest
import json
import os
from flask import Flask

from server.handler.routes import main 
from server.model.form import Form
from server.model.encoder import Encoder
from server.service.process import load
from server.service.s3 import create_bucket, clean_up
from server.config import config

class TestSubmitFiles(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(main)
        self.client = self.app.test_client()

        current_config = config[os.getenv('RUN_MODE','default')]

        self.secret = current_config.SECRET 
        self.url = current_config.URL
        self.key = current_config.KEY


        load()
        # create the dev bucket if it doesn't exist
        create_bucket("dev-bucket",self.url,self.key,self.secret)        

    def tearDown(self):
        clean_up(self.url,self.key,self.secret)               

    def test_submit_files_success(self):
        # Test successful JSON submission
        form = Form(user_id="hello",app_id="1234",app_language="java",config_text="blah")
        json_str = json.dumps(form,cls=Encoder)
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