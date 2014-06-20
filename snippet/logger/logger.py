import logging

from handler import HandlerFactory
import settings


def config_logger(logger):
    name = logger.name
    logger.addHandler(HandlerFactory.get_fh(name))
    logger.addHandler(HandlerFactory.get_rh(settings.LOG_REDIS_CHANNEL))
    logger.addHandler(HandlerFactory.get_ch())
    logger.setLevel(settings.LOG_LEVEL)


def get_logger(key='snippet'):
    logger = _logger_dict.get(key)
    if logger is not None:
        return logger
    logger = logging.getLogger(key)
    config_logger(logger)
    _logger_dict[key] = logger
    return logger


_logger_dict = {}
log = get_logger()