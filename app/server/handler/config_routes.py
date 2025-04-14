from loguru import logger

from flask import Blueprint, request

from .config import Config
from server.model.encoder import class_to_json

cfg = Blueprint('cfg',__name__)

@cfg.route("/api/config/<env>", methods=["GET"])
def get_config(env):
    logger.info(f"{request.method}, {request.path}, is_json={request.is_json}")
    logger.debug(f"env={env}")

    # S3 config with secrets redacted
    config = Config
    config.s3_secret_access_key = ""
    config.llm_key = ""

    logger.debug(f"config={config}")
    return class_to_json(config), 200

