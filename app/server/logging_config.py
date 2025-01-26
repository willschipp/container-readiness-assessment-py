import logging

def setup_logging():
    # logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # set handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    # formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    # add the handler
    logger.addHandler(console_handler)
    # return
    return logger