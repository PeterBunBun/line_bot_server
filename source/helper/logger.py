import logging
import os

from source.global_config import GlobalConfigs


def getProgramLogger(logging_file_name):
    os.makedirs(GlobalConfigs.LOG_DIR, exist_ok=True)

    logfile = GlobalConfigs.LOG_DIR + logging_file_name + '.log'

    logger = logging.getLogger(logging_file_name)
    logger.setLevel(logging.DEBUG)
    fhandlr = logging.FileHandler(filename=logfile)
    formatter = logging.Formatter('%(asctime)s - %(filename)s - %(lineno)s - %(levelname)s - %(message)s')
    fhandlr.setFormatter(formatter)
    logger.addHandler(fhandlr)

    strhandlr = logging.StreamHandler()
    strhandlr.setFormatter(formatter)
    logger.addHandler(strhandlr)

    return logger
