import unittest
import os
import json

from server.service.llm import call_gemini, escape_other_for_json, escape_xml_for_json, clean_string

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
        escaped_code = escape_other_for_json(content)
        # build a json object
        json_obj = {
            "body":"stuff " + escaped_code
        }
        # convert to json string
        json_string = json.dumps(json_obj)
        is_valid = False
        try:
            json.loads(json_string)
            is_valid = True
        except json.JSONDecodeError:
            is_valid = False
        self.assertTrue(is_valid)

    def test_escape_xml_for_json(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir,'./examples/spring_boot_pom.xml')
        # load up the file
        with open(file_path,'r') as input:
            content = input.read()
        escaped_code = escape_xml_for_json(content)
        # build a json object
        json_obj = {
            "body":"stuff " + escaped_code
        }
        # convert to json string
        json_string = json.dumps(json_obj)
        is_valid = False
        try:
            json.loads(json_string)
            is_valid = True
        except json.JSONDecodeError:
            is_valid = False
        self.assertTrue(is_valid)        

    def test_clean_string(self):
        # try and xml first
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir,'./examples/spring_boot_pom.xml')
        # load up the file
        with open(file_path,'r') as input:
            content = input.read()
        escaped_code = clean_string(content)
        # build a json object
        json_obj = {
            "body":"stuff " + escaped_code
        }
        # convert to json string
        json_string = json.dumps(json_obj)
        is_valid = False
        try:
            json.loads(json_string)
            is_valid = True
        except json.JSONDecodeError:
            is_valid = False
        self.assertTrue(is_valid)
        # now do a json file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir,'./examples/spring_boot_build.gradle')
        # load up the file
        with open(file_path,'r') as input:
            content = input.read()
        escaped_code = clean_string(content)
        # build a json object
        json_obj = {
            "body":"stuff " + escaped_code
        }
        # convert to json string
        json_string = json.dumps(json_obj)
        is_valid = False
        try:
            json.loads(json_string)
            is_valid = True
        except json.JSONDecodeError:
            is_valid = False
        self.assertTrue(is_valid)        



if __name__ == '__main__':
    unittest.main()