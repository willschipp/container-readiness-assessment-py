import os
from loguru import logger
from server.exceptions.validation_exception import ValidationException


def validate_file_exists(file_name: str):
    logger.info(f": file_name: '{file_name}'")

    if os.path.isfile(file_name) is False:
        raise ValidationException(f"File {file_name} required")
