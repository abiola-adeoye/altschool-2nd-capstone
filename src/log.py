import os
import logging


def load_logging(name):
    # create a custom logger and set to INFO level
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # create logging format
    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # check log file path, create if not exist
    log_file_path = os.path.abspath("log_records/")
    if not os.path.exists(log_file_path):
        os.makedirs(log_file_path)

    # create handlers
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(f"{log_file_path}/{name}.log")

    # setting the format the log records will be saved
    console_handler.setFormatter(log_format)
    file_handler.setFormatter(log_format)

    # add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger
