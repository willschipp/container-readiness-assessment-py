import unittest
import json

from server.model.encoder import Encoder, load_prompts
from server.model.form import Form

class TestFormEncoder(unittest.TestCase):

    def test_obj(self):
        # do something
        form = Form("user123","app123","java","some config text here")
        # serialize to json
        json_str = json.dumps(form,cls=Encoder)
        expected_json = {
            "user_id":"user123",
            "app_id":"app123",
            "app_language":"java",
            "config_text":"some config text here"
        }
        self.assertEqual(json.loads(json_str),expected_json)

    def test_loadPrompts(self):
        prompts = load_prompts()
        self.assertTrue(len(prompts) >= 4)



if __name__ == '__main__':
    unittest.main()