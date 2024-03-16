import logging
import logging.handlers
import os

LOG_DIR = "logs"
LOG_PATH = os.path.join(LOG_DIR, "chat-csv.log")


def setup_logging():
    """
    Setup the chat-csv logger.

    Return:
        logger object
    """
    logger = logging.getLogger(name="chat-csv")
    logger.setLevel(logging.DEBUG)

    # Log format
    default_format = logging.Formatter("[%(asctime)s] [%(levelname)s] - %(message)s")

    if not os.path.exists(LOG_DIR):
        try:
            os.mkdir(LOG_DIR)
        except OSError as e:
            logger.error("Exception when creating {}: {}".format(LOG_DIR, e))

    file_handler = logging.handlers.TimedRotatingFileHandler(
        filename=LOG_PATH,
        when="midnight",
        interval=1,
        encoding="utf-8",
    )

    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(fmt=default_format)

    # Console Handler for stdout
    streamhandler = logging.StreamHandler()
    streamhandler.setLevel(logging.INFO)
    streamhandler.setFormatter(fmt=default_format)

    # Adding Handler
    logger.addHandler(file_handler)
    logger.addHandler(file_handler)

    return logger


logger = setup_logging()
