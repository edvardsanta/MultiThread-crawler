import logging

def log(message):
    logger_format = '%(asctime)s: %(threadName)s: %(message)s'
    logging.basicConfig(format=logger_format, level=logging.INFO, datefmt="%H:%M:%S")


    logging.info(message)