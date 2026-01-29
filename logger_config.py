import logging


def setup_logger():
    logger = logging.getLogger("Parser")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(levelname)s: %(message)s. %(asctime)s", datefmt="%H:%M:%S"
    )

    file_handler = logging.FileHandler("ozby_parser.log", encoding="utf-8")
    file_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)

    return logger


logger = setup_logger()
