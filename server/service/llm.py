import requests

from ..model.response import GeminiReponse
from ..config import config

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

def callGemini(prompt: str) -> str:
    current_config = config['dev']

    final_prompt = gemini_request_template.replace("CONTENT_HERE",prompt)
    url = current_config.LLM_URL
    url = url.replace("API_KEY",current_config.LLM_KEY)

    print(final_prompt)

    try:
        headers = {"Content-type":"application/json"}
        response = requests.post(url,data=final_prompt,headers=headers)
        # process response body into the json object
        response.raise_for_status()
        return str(response.json)
    except requests.exceptions.RequestException as err:
        print(f"an error occurred: {err}")
        return None

