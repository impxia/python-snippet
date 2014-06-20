import os
import json
import redis
import threading
from datetime import datetime

import settings

redis_conf = settings.REDIS_CONF
r = redis.StrictRedis(host=redis_conf['host'], port=redis_conf['port'], db=redis_conf['db'])


class Listener(threading.Thread):
    def __init__(self, r, channels):
        threading.Thread.__init__(self)
        self.redis = r
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(channels)

    def write(self, item, f):
        try:
            dict_data = json.loads(item['data'])
            time = dict_data['created']
            date = datetime.fromtimestamp(time)
            format_data = {
                'asctime': str(date),
                'name': dict_data['name'],
                'host': dict_data['host'],
                'levelname': dict_data['levelname'],
                'message': dict_data['msg'],
                'filename': dict_data['filename'],
                'funcName': dict_data['funcName']
            }
            log = '[%(asctime)s] - [%(name)s] - [%(host)s] - [%(levelname)s] - [%(filename)s] - [%(funcName)s] - %(message)s' % format_data
            f.writelines(log + "\n")
            f.flush()
        except:
            pass

    def run(self):
        path = settings.LOG_FOLDER
        log_root = os.path.join(path, 'all')
        if not os.path.exists(log_root):
            os.makedirs(log_root)
        file = settings.CENTRAL_LOG_FILE
        filepath = os.path.join(log_root, file)
        with open(filepath, 'a') as f:
            flush_count = 0
            for item in self.pubsub.listen():
                self.write(item, f)
                flush_count = (flush_count + 1) % 100
                if flush_count == 0:
                    f.flush()


def start_logger():
    client = Listener(r, [settings.LOG_REDIS_CHANNEL])
    client.start()
    print 'Log recorder started running.'


if __name__ == "__main__":
    start_logger()