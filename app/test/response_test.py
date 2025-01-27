import unittest
import os

from server.model.response import parse_json_to_gemini_response


class TestResponse(unittest.TestCase):

    def setUp(self):
        pass

    def test_parse_json_to_gemini_response(self):
        # read in the file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir,'./examples/gemini_yes.json')
        # load up the file
        with open(file_path,'r') as input:
            content = input.read()
        # convert to json
        response = parse_json_to_gemini_response(content)
        self.assertIsNotNone(response)
        self.assertTrue(response.candidates[0].content.parts[0].text == "Yes \n")

if __name__ == '__main__':
    unittest.main()    