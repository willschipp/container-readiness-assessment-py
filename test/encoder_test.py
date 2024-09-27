import unittest
import json

from server.model.encoder import Encoder, loadPrompts
from server.model.form import Form

class TestFormEncoder(unittest.TestCase):

    def test_obj(self):
        # do something
        form = Form("user123","app123","java","some config text here")
        # serialize to json
        json_str = json.dumps(form,cls=Encoder)
        expected_json = {
            "userid":"user123",
            "appid":"app123",
            "applanguage":"java",
            "configtext":"some config text here"
        }
        self.assertEqual(json.loads(json_str),expected_json)

    def test_loadPrompts(self):
        prompts = loadPrompts()
        self.assertTrue(len(prompts) >= 4)



if __name__ == '__main__':
    unittest.main()