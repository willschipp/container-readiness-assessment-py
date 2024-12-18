from flask import Flask, send_from_directory
import logging
import os

from .logging_config import setup_logging
from .handler.routes import main as main_blueprint
from .handler.config_routes import cfg as main_config
from .service.process import start_background

logger = setup_logging()

def init_app(config_name='default'):
    # app = Flask(__name__,static_folder='../frontend/build',static_url_path='/')
    app = Flask(__name__,static_folder='../frontend/build')
    app.register_blueprint(main_blueprint)
    app.register_blueprint(main_config)
    return app

app = init_app(os.getenv('FLASK_CONFIG') or 'default')

# star the processing
start_background()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    logger.info("starting...")    
    app.run()