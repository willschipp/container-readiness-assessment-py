import sys
import logging
from loguru import logger
from server.configuration import settings
from server.exceptions.log_level_exception import LogLevelException

# logger class
class Log:

    @staticmethod
    def setup_default():

        logger.info("Configure default log handlers")

        logger.remove(0)  # Remove default handler
        logger.add(  # Add default handler to stderr
            sys.stderr, backtrace=True, level=settings.log_level
        )
        logger.add(  # Add handler to file
            settings.log_file,
            backtrace=True,
            level=settings.log_level,
            rotation=settings.log_file_rotation,
            retention=settings.log_file_retention_days,
        )

    @staticmethod
    def get_log_level_int():
        match settings.log_level:
            case "INFO":
                return logging.INFO  # 20
            case "DEBUG":
                return logging.DEBUG  # 10
            case "WARNING":
                return logging.WARNING  # 30
            case "ERROR":
                return logging.ERROR  # 40
            case "CRITICAL":
                return logging.CRITICAL  # 50
            case _:
                raise LogLevelException(f"Unknown level={settings.log_level}")


class FlaskInterceptHandler(logging.Handler):
    def emit(self, record):
        # Retrieve context where the logging call occurred, this happens to be in the 6th frame upward
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelname, record.getMessage())

    @staticmethod
    def setup_default():
        logging.basicConfig(handlers=[FlaskInterceptHandler()], level=0)
