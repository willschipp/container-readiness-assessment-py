from flask import Blueprint, send_file, request, jsonify

from logging_config import setup_logging
from config import config
from model.encoder import class_to_json

cfg = Blueprint('cfg',__name__)

logger = setup_logging()

@cfg.route('/api/config/<env>',methods=['GET'])
def get_config(env):
    logger.info("getting config")
    current_config = config[env]
    # scrub anything in this that is called 'secret' or 'key'
    current_config.SECRET = ""
    current_config.LLM_KEY = ""
    # return
    return class_to_json(current_config),200
