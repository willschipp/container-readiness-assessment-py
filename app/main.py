import os
from loguru import logger
from flask import Flask, send_from_directory
from flask_cors import CORS
from server.configuration import settings, Configuration
from server.utils.log import Log, FlaskInterceptHandler
from server.handler.routes import main as main_blueprint
from server.handler.config_routes import cfg as main_config
from server.handler.prompt_routes import prompt_handler as prompt_config
from server.service.process import start_background

# Logger default
Log.setup_default()  # Must be first code executed

# Flask server
app = Flask(__name__, static_folder="frontend/build")
app.register_blueprint(main_blueprint)
app.register_blueprint(main_config)
app.register_blueprint(prompt_config)
FlaskInterceptHandler.setup_default()
CORS(app)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(app.static_folder + "/" + path):
        logger.debug(f"app.static_folder={app.static_folder}, path={path}")
        return send_from_directory(app.static_folder, path)
    else:
        logger.debug(f"app.static_folder={app.static_folder}, path=index.html")
        return send_from_directory(app.static_folder, "index.html")


@logger.catch
def main():
    """Main."""
    logger.info("")

    # Configuration
    Configuration.validate()

    logger.info(f"log_level={settings.log_level}")
    logger.info(f"environment={settings.env_for_dynaconf}")

    # Background jobs
    run_background = os.getenv('BACKGROUND','run')
    if run_background == 'run':
        start_background()


    # Flask
    app.run(
        host=settings.flask_host,
        port=settings.flask_port,
        threaded=True,
    )


if __name__ == "__main__":
    """__main__

    Run when executed as a script.
    """
    logger.info("")

    try:
        main()

    except Exception as e:
        logger.error(f"Exited due to exception: {e}")
        raise e  # Get traceback
