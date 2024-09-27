from flask import Flask
import logging
import os

from .logging_config import setup_logging
from .handler.routes import main as main_blueprint

logger = setup_logging()

def init_app(config_name='default'):
    app = Flask(__name__)
    app.register_blueprint(main_blueprint)
    return app

app = init_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == "__main__":
    logger.info("starting...")
    app.run()