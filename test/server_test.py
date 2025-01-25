import unittest
import json
import os

from server.server import init_app
from server.model.form import Form
from server.model.encoder import Encoder

from server.service.process import load
from server.service.s3 import create_bucket, clean_up

class TestServer(unittest.TestCase):

    def setUp(self):
        self.app = init_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.secret = os.getenv("SECRET")
        self.url = "localhost:9000"
        self.key = "Fkr0MyVrlIufkEyvWZ4z"

        load()
        # create the dev bucket if it doesn't exist
        create_bucket("dev-bucket",self.url,self.key,self.secret)        

    def tearDown(self):
        self.app_context.pop()
        clean_up(self.url,self.key,self.secret)               


    def test_submit_files(self):
        form = Form(user_id="userid",app_id="blah",app_language="java",config_text="other")
        response = self.client.post('/api/order',
                                    data=json.dumps(form,cls=Encoder),
                                    content_type='application/json')        
        self.assertEqual(response.status_code,200)


if __name__ == '__main__':
    unittest.main()