from flask import Blueprint, send_from_directory, render_template, request, jsonify
import logging
import os

from ..logging_config import setup_logging

from ..model.form import Form
from ..model.prompt import Prompt
from ..model.encoder import load_prompts

from ..service.process import create_job
from ..service.order_management import get_job_by_order_id

logger = setup_logging()

prompts = []

main = Blueprint('main',__name__)

def load():
    global prompts
    if len(prompts) <= 0:
        logger.info("prompts loaded")
        prompts = load_prompts()

@main.route('/api/order',methods=['POST'])
def submit_files():
    logger.info("order")
    if request.is_json:
        data = request.get_json()

        if len(data) <= 0:
            return jsonify({
                "error":"no payload"
            }), 500
        
        form = Form.from_dict(data)

        # create an order id and send it back
        orderid = create_job(form)

        logger.info("job " + orderid + " created")
        return jsonify({
            "orderid":orderid
        }), 200
    else:
        logger.error("Not a json file")
        return jsonify({
            "error":"parsing json"
        }), 400
    
@main.route('/api/order/<order_id>',methods=['GET'])
def get_order(order_id):
    logger.info("get order")
    order = get_job_by_order_id(order_id)
    return jsonify(order),200


@main.route('/api/languages',methods=['GET'])
def get_languages():
    logger.info("getting languages")
    #load the prompts
    load()
    # get all the app languages
    app_languages = []
    for p in prompts:
        if p.app_language not in app_languages:
            if p.app_language != 'any': # ignore 'any' --> keyword
                app_languages.append(p.app_language)
    
    return jsonify({
        "languages":app_languages
    }),200


    