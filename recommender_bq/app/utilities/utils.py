import sys
import logging

class Utils:
    _SUCCESS_ = 'success'
    _DATA_ = 'data'
    _ERROR_ = 'error'
    _MESSAGE_ = 'message'
    _ID_ = 'id'

    @staticmethod
    def standard_response(success=True, data='none', error=None, message='ok'):
        return {
            Utils._SUCCESS_: success,
            Utils._DATA_: data,
            Utils._ERROR_: error,
            Utils._MESSAGE_: message
        }

    @staticmethod
    def get_console_handler():
        console_format = logging.Formatter(
            "%(filename)s:%(lineno)d - %(levelname)s — %(message)s")

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(console_format)
        return console_handler

    @staticmethod
    def get_logger():
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(Utils.get_console_handler())
        logger.propagate = False
        return logger
