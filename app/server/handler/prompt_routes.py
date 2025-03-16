from flask import Blueprint, send_file, request, jsonify
import tempfile
import logging
import json
import os

from server.model.encoder import load_prompts
from server.model.prompt import Prompt

from server.service.process import reset_prompts, get_prompts

logger = logging.getLogger("handler.prompt_routes")

# globals
prompts = []

prompt_handler = Blueprint('prompt_handler',__name__)

def load():
    global prompts
    logger.info("prompts loaded")
    prompts = get_prompts()


@prompt_handler.route('/api/prompts',methods=['GET'])
def get_orders():
    load()
    logger.info("getting all orders")
    return jsonify(prompts),200


@prompt_handler.route('/api/prompts',methods=['POST'])
def submit_prompts():
    if request.is_json:
        data = request.get_json()

        if len(data) <= 0:
            return jsonify({
                "error":"no payload"
            }), 500
        
        
        try:
            # loop through data
            for data_prompt in data:
                Prompt.from_dict(data_prompt)
                # TODO validate if p has all the bits
                # it parses
        except Exception as e:
            logger.error("error parsing submission {e}")
            return jsonify({
                "error":"parsing json"
            }), 400

        prompt_dict = {"prompts":data}

        # write it to a location and then pass it on to the process
        with tempfile.NamedTemporaryFile(mode="w+",delete=False,suffix=".json") as temp_file:
            # temp_file.write(prompt_dict)
            json.dump(prompt_dict,temp_file)
            temp_file_path = temp_file.name
            temp_file.close() #flush

        logger.info(temp_file_path)

        # upload
        reset_prompts(temp_file_path)

        # clean up
        os.remove(temp_file_path)

        # reset the prompts
        logger.info("prompts updated")
        return jsonify({}),204
    else:
        logger.error("Not a json file")
        return jsonify({
            "error":"parsing json"
        }), 400