from flask import Flask
import logging
import os

from .logging_config import setup_logging
from .handler.routes import main as main_blueprint
from .service.process import start_background

logger = setup_logging()

def init_app(config_name='default'):
    app = Flask(__name__)
    app.register_blueprint(main_blueprint)
    return app

app = init_app(os.getenv('FLASK_CONFIG') or 'default')

# star the processing
start_background()

if __name__ == "__main__":
    logger.info("starting...")    
    app.run()