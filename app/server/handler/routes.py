from flask import Blueprint, send_file, request, jsonify
import tempfile
from loguru import logger
import json

from server.model.form import Form
from server.model.encoder import load_prompts

from server.service.process import create_job
from server.service.order_management import get_job_by_order_id, get_all_orders
from server.service.s3 import get_file, list_files_in_folder


prompts = []

main = Blueprint('main',__name__)

def load():
    global prompts

    if len(prompts) <= 0:
        logger.info("prompts loaded")
        prompts = load_prompts()

@main.route('/api/order',methods=['POST'])
def submit_files():
    logger.info(f"{request.method}, {request.path}, is_json={request.is_json}")
    if request.is_json:
        data = request.get_json()

        if len(data) <= 0:
            return jsonify({
                "error":"no payload"
            }), 500
        
        form = Form.from_dict(data)
        # create an order id and send it back
        orderid = create_job(form)

        logger.info(f"job {orderid}created")
        return jsonify({
            "orderid":orderid
        }), 200
    else:
        logger.error("Not a json file")
        return jsonify({
            "error":"parsing json"
        }), 400

@main.route('/api/order',methods=['GET'])
def get_orders():
    logger.info(f"{request.method}, {request.path}, is_json={request.is_json}")
    orders = get_all_orders()
    return jsonify(orders),200

@main.route('/api/order/<order_id>',methods=['GET'])
def get_order(order_id):
    logger.info(f"{request.method}, {request.path}, is_json={request.is_json}")
    order = get_job_by_order_id(order_id)
    return jsonify(order),200


@main.route('/api/languages',methods=['GET'])
def get_languages():
    logger.info(f"{request.method}, {request.path}, is_json={request.is_json}")
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


@main.route('/api/order/<order_id>/files',methods=['GET'])
def get_files_list(order_id):
    logger.info(f"{request.method}, {request.path}, is_json={request.is_json}")
    try :
        files = list_files_in_folder(order_id)
        response = []
        for file in files:
            if '.json' not in file:
                response.append(file)
        return jsonify(response),200
    except Exception as err:
        return jsonify({
            "error":err
        }),500
    
@main.route('/api/order/<order_id>/answer',methods=['GET'])
def get_answers(order_id):
    logger.info(f"{request.method}, {request.path}, is_json={request.is_json}")
    try :
        files = list_files_in_folder(order_id)
        response = []
        for file in files:
            if 'answer' in file:
                response.append(file)
        return jsonify(response),200
    except Exception as err:
        return jsonify({
            "error":err
        }),500    

@main.route('/api/order/<order_id>/answer/<file_name>',methods=['GET'])
def get_answer(order_id,file_name):
    logger.info(f"{request.method}, {request.path}, is_json={request.is_json}")
    # get the explicit file, read it and stream the response to the browser
    try:
        with tempfile.NamedTemporaryFile(mode="w+",delete=False,suffix=".tmp") as temp_file:
            pass

        object_name = f"{order_id}/{file_name}"

        get_file(object_name, temp_file.name)
        with open(temp_file.name,'r') as answer_file:
            data = json.load(answer_file)            
        return jsonify(data),200    
    except Exception as err:
        return jsonify({
            "error":err
        }),500


@main.route('/api/download/<order_id>/<file_id>',methods=['GET'])
def download_file(order_id,file_id):
    logger.info(f"{request.method}, {request.path}, is_json={request.is_json}")
    try:
        # setup the temporary file
        # download from s3
        # stream back
        with tempfile.NamedTemporaryFile(mode="w+",delete=False,suffix=".tmp") as temp_file:
            pass

        object_name = f"{order_id}/{file_id}"
        # current_config = config[os.getenv('RUN_MODE','dev')]
        # get_file(temp_file.name,order_id,file_id,current_config.URL,current_config.KEY,current_config.SECRET)
        get_file(object_name, temp_file.name)
        # serve
        return send_file(temp_file.name,as_attachment=True,download_name=file_id)
        # TODO clean up
    except Exception as err:
        return jsonify({
            "error":err
        }),500
    
@main.route('/api/order/<order_id>/file/<file_id>/stream',methods=['GET'])
def stream_file(order_id,file_id):
    logger.info(f"{request.method}, {request.path}, is_json={request.is_json}")
    try:
        # setup the temporary file
        # download from s3
        # stream back
        with tempfile.NamedTemporaryFile(mode="w+",delete=False,suffix=".tmp") as temp_file:
            pass

        object_name = f"{order_id}/{file_id}"
        # current_config = config[os.getenv('RUN_MODE','dev')]
        # get_file(temp_file.name,order_id,file_id,current_config.URL,current_config.KEY,current_config.SECRET)
        get_file(object_name, temp_file.name)
        # serve
        with open(temp_file.name,'r') as usable_file:
            file_content = usable_file.read()            
        return file_content, 200, {'Content-type':'text/plain'}
    except Exception as err:
        return jsonify({
            "error":err
        }),500


    