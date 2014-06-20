from snippet.logger.logger import log


# start logger before this test
# from snippet.logger import log_recorder
# log_recorder.start_logger()

def test():
    log.debug('test logging')