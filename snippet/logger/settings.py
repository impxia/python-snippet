import os

REDIS_CONF = {'host': 'localhost',
              'port': 6379,
              'db': 0}
LOG_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'log')
LOG_LEVEL = 'DEBUG'
LOG_REDIS_CHANNEL = 'SNIPPET_LOG'
CENTRAL_LOG_FILE = 'snippet.log'