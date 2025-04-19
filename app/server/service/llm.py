import json
import logging
import requests
import os
from loguru import logger

import xml.etree.ElementTree as Element

import server.constants as constants
from server.configuration import settings
from server.model.response import GeminiResponse

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

ollama_request_template = '''
    {
        "model":"codellama:latest",
        "prompt":"CONTENT_HERE",
        "format":"json",
        "stream":false
    }
'''

llamacpp_request_template = '''
    {
        "prompt":"CONTENT_HERE"
    }
'''

def call_llm(prompt: str,name: str) -> str:
    if name == constants.LLM_NAME_GEMINI:
        return call_gemini(prompt)
    elif name == constants.LLM_NAME_OLLAMA:
        return call_ollama(prompt)
    elif name == constants.LLM_NAME_LLAMACPP:
        return call_llamacpp(prompt)
    else:
        raise Exception(f"Unknown name={name}")

def call_gemini(prompt: str) -> str:
    try:
        final_prompt = gemini_request_template.replace("CONTENT_HERE",prompt)
        url = settings.llm_url_gemini
        url = url.replace("API_KEY",settings.LLM_KEY)
        headers = {constants.CONTENT_TYPE:constants.CONTENT_TYPE_JSON}
        # send
        response = requests.post(url,data=final_prompt,headers=headers)
        response.raise_for_status()
        response_string = json.dumps(response.json())
        return response_string
    except requests.exceptions.RequestException as err:
        logging.error(f"an error occurred: {err.args[0]}")
        return None


def call_ollama(prompt: str) -> str:

    final_prompt = ollama_request_template.replace("CONTENT_HERE",prompt)
    url = settings.llm_url_ollama
    
    logging.info(final_prompt)

    try:
        headers = {constants.CONTENT_TYPE:constants.CONTENT_TYPE_JSON}
        response = requests.post(url,data=final_prompt,headers=headers)
        # process response body into the json object
        response.raise_for_status()
        response_string = json.dumps(response.json())
        return response_string
    except requests.exceptions.RequestException as err:
        logging.error(f"an error occurred: {err.args[0]}")
        return None
    

def call_llamacpp(prompt: str) -> str:

    final_prompt = llamacpp_request_template.replace("CONTENT_HERE",prompt)
    url = settings.llm_url_llamacpp
    
    logging.debug(final_prompt)

    try:
        headers = {constants.CONTENT_TYPE:constants.CONTENT_TYPE_JSON}
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