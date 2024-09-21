import unittest
import json

from server.model.form_encoder import FormEncoder
from server.model.form import Form

class TestFormEncoder(unittest.TestCase):

    def test_obj(self):
        # do something
        form = Form("user123","app123","java","some config text here")
        # serialize to json
        json_str = json.dumps(form,cls=FormEncoder)
        expected_json = {
            "userid":"user123",
            "appid":"app123",
            "applanguage":"java",
            "configtext":"some config text here"
        }
        self.assertEqual(json.loads(json_str),expected_json)



if __name__ == '__main__':
    unittest.main()