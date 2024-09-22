from flask import Flask
import os

from .handler.routes import main as main_blueprint

def init_app(config_name='default'):
    app = Flask(__name__)
    app.register_blueprint(main_blueprint)
    return app

app = init_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == "__main__":
    app.run()