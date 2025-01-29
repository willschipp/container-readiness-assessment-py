from flask import Blueprint, send_file, request, jsonify
import tempfile
import logging
import json
import os

from model.encoder import load_prompts
from model.prompt import Prompt

from service.process import reset_prompts

logger = logging.getLogger("handler.prompt_routes")

# globals
prompts = []

main = Blueprint('prompts',__name__)

def load():
    global prompts
    if len(prompts) <= 0:
        logger.info("prompts loaded")
        prompts = load_prompts()


@main.route('/api/prompts',methods=['GET'])
def get_orders():
    logger.info("getting all orders")
    return jsonify(prompts),200


@main.route('/api/prompts',methods=['POST'])
def submit_prompts():
    logger.info("prompts")
    if request.is_json:
        data = request.get_json()

        if len(data) <= 0:
            return jsonify({
                "error":"no payload"
            }), 500
        
        prompts = Prompt.from_dict(data)
        # write it to a location and then pass it on to the process
        with tempfile.NamedTemporaryFile(mode="w+",delete=False,suffix=".json") as temp_file:
            temp_file.write(prompts)
            temp_file_path = temp_file.name

        # upload
        reset_prompts(temp_file_path)

        # clean up
        os.remove(temp_file_path)

        # reset the prompts
        logger.info("prompts updated")
        return 204
    else:
        logger.error("Not a json file")
        return jsonify({
            "error":"parsing json"
        }), 400