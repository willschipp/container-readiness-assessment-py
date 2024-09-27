import json
import logging
import requests


import xml.etree.ElementTree as Element

from ..model.response import GeminiResponse
from ..config import config
from ..logging_config import setup_logging

logger = setup_logging()

# Gemini Request Payload
gemini_request_template = '''
    {
    "contents":
        [
            {
            "parts":
                [
                    {"text":"CONTENT_HERE"}
                ]
            }
        ]
    }
'''

def call_gemini(prompt: str) -> str:
    current_config = config['dev']

    final_prompt = gemini_request_template.replace("CONTENT_HERE",prompt)
    url = current_config.LLM_URL
    url = url.replace("API_KEY",current_config.LLM_KEY)

    logging.debug(final_prompt)

    try:
        headers = {"Content-type":"application/json"}
        response = requests.post(url,data=final_prompt,headers=headers)
        # process response body into the json object
        response.raise_for_status()
        response_string = json.dumps(response.json())
        return response_string
    except requests.exceptions.RequestException as err:
        logging.error(f"an error occurred: {err}")
        return None


def escape_xml_for_json(xml_string):
    # First, escape special characters in the XML
    escaped_xml = xml_string.replace('&', '&amp;')
    escaped_xml = escaped_xml.replace('<', '&lt;')
    escaped_xml = escaped_xml.replace('>', '&gt;')
    escaped_xml = escaped_xml.replace('"', '&quot;')
    escaped_xml = escaped_xml.replace("'", '&apos;')
    
    # Then, escape the result for JSON
    json_escaped_xml = json.dumps(escaped_xml)
    
    # Remove the surrounding quotes added by json.dumps()
    return json_escaped_xml[1:-1]

def escape_other_for_json(code):
    # Remove any leading/trailing whitespace
    code = code.strip()
    
    # Use json.dumps() to properly escape the string
    escaped_code = json.dumps(code)
    
    # Remove the surrounding quotes added by json.dumps()
    escaped_code = escaped_code[1:-1]
    
    return escaped_code

def clean_string(code):
    # check what type of string it is (XML or other)
    try:
        Element.fromstring(code) # convert to XML
        # if we made it here - it's XML        
        return escape_xml_for_json(code)
    except Element.ParseError:
        # if we're here, it's not XML
        return escape_other_for_json(code)