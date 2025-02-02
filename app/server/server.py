from flask import Flask, send_from_directory
from flask.logging import default_handler
from logging_config import setup_logging

import os
import sys

from handler.routes import main as main_blueprint
from handler.config_routes import cfg as main_config
from handler.prompt_routes import prompt_handler as prompt_config
from service.process import start_background


# initial checks for keys being set
if 'SECRET' not in os.environ:
    print("SECRET for s3 not set... exiting\n")
    sys.exit(1)

def init_app(config_name='default'):
    app = Flask(__name__,static_folder='../frontend/build')
    app.register_blueprint(main_blueprint)
    app.register_blueprint(main_config)
    app.register_blueprint(prompt_config)
    # logging
    setup_logging()
    app.logger.removeHandler(default_handler) # remove the default

    return app

# initiate the app
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
    app.logger.info("starting...")    
    app.run(host='0.0.0.0',port=5000,threaded=True)