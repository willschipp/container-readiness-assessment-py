from flask import Flask
import logging
import os

from .logging_config import setup_logging
from .handler.routes import main as main_blueprint
from .handler.config_routes import cfg as main_config
from .service.process import start_background

logger = setup_logging()

def init_app(config_name='default'):
    app = Flask(__name__,static_folder='../frontend/build',static_url_path='/')
    app.register_blueprint(main_blueprint)
    app.register_blueprint(main_config)
    return app

app = init_app(os.getenv('FLASK_CONFIG') or 'default')

# star the processing
start_background()

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == "__main__":
    logger.info("starting...")    
    app.run()