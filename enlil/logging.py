import logging

def setup_log():
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
