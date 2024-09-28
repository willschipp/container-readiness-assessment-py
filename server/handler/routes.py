from flask import Blueprint, send_from_directory, render_template, request, jsonify
import logging
import os

from ..logging_config import setup_logging

from ..model.form import Form
from ..model.order import Order

from ..service.process import create_job
from ..service.order_management import get_job_by_order_id

logger = setup_logging()

main = Blueprint('main',__name__)

@main.route('/')
def home():
    logger.info("returning index")
    return render_template('index.html')

@main.route('/static/<path:filename>')
def serve_static(filename):
    logger.info("returning static")
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir,'static'),"index.html")    

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

    