import unittest
import os
import json

from server.service.llm import callGemini, escape_gradle_for_json

class TestProcess(unittest.TestCase):

    def setUp(self):
        pass

    # def test_callGemini(self):
    #     result = callGemini("why is the sky blue?")
    #     print(result)

    def test_escape_gradle_for_json(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir,'./examples/spring_boot_build.gradle')
        # load up the file
        with open(file_path,'r') as input:
            content = input.read()
        escaped_code = escape_gradle_for_json(content)
        self.assertTrue(len(escaped_code) > 0)
        # add to a json fragment
        json_st = {
            "body":escaped_code
        }

        json_string = json.dumps(json_st,indent=None,sort_keys=False)
        print(json_st)



if __name__ == '__main__':
    unittest.main()