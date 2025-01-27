import logging

from flask import Blueprint, request

from config import config
from model.encoder import class_to_json

cfg = Blueprint('cfg',__name__)

logger = logging.getLogger("handler.config_routes")

@cfg.route('/api/config/<env>',methods=['GET'])
def get_config(env):
    logger.info("getting config")
    current_config = config[env]
    # scrub anything in this that is called 'secret' or 'key'
    current_config.SECRET = ""
    current_config.LLM_KEY = ""
    # return
    return class_to_json(current_config),200
