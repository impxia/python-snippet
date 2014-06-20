import os
import socket
import json
import logging
import redis
import settings

hostname = socket.gethostname()
formatter = logging.Formatter(
    '[%(asctime)s] - [%(name)s] - [' + hostname + '] - [%(levelname)s] - [%(filename)s] - [%(funcName)s] - %(message)s')


class RedisHandler(logging.Handler):
    def __init__(self, channel, conn, *args, **kwargs):
        logging.Handler.__init__(self, *args, **kwargs)
        self.channel = channel
        self.redis_conn = conn

    def emit(self, record):
        attributes = [
            'name', 'msg', 'levelname', 'levelno', 'pathname', 'filename',
            'module', 'lineno', 'funcName', 'created', 'msecs', 'relativeCreated',
            'thread', 'threadName', 'process', 'processName',
        ]
        record_dict = dict((attr, getattr(record, attr)) for attr in attributes)
        record_dict['formatted'] = self.format(record)
        record_dict['host'] = hostname
        try:
            self.redis_conn.publish(self.channel, json.dumps(record_dict))
        except redis.RedisError:
            pass


class HandlerFactory():
    @staticmethod
    def get_rh(channel):
        conf = settings.REDIS_CONF
        r = redis.StrictRedis(host=conf['host'], port=conf['port'], db=conf['db'])
        return RedisHandler(channel, r)

    @staticmethod
    def get_fh(key):
        log_root = os.path.join(settings.LOG_FOLDER, 'this')
        if not os.path.exists(log_root):
            os.makedirs(log_root)
        filename = '%s.log' % key
        filepath = os.path.join(log_root, filename)
        fh = logging.FileHandler(filepath)
        fh.setFormatter(formatter)
        return fh

    @staticmethod
    def get_ch():
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        return ch