import logging
import os


def Logger(this):
    """
    Sets up the logger to save logs to a file.

    :param log_file: Name of the log file.
    :return: Configured logger.
    """
    logger = logging.getLogger(this)
    logger.setLevel(logging.DEBUG)

    # Create a file handler
    file_handler = logging.FileHandler("app.log")
    file_handler.setLevel(logging.DEBUG)

    # Create a formatter and add it to the handler
    formatter = logging.Formatter(
        "%(asctime)s - file:'%(name)s' - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(file_handler)

    return logger
