# -*- coding: utf-8 -*-
import uuid
import logging as sys_logging
import threading

LOG_THREAD_VALUE = threading.local()


def getLogger(name=None):
    logger = sys_logging.getLogger(name)
    return MyLogger(logger)


def clear_trace():
    try:
        del LOG_THREAD_VALUE.trace_id
    except AttributeError:
        pass


class MyLogger(object):
    def __init__(self, logger):
        self.inner_logger = logger

    @staticmethod
    def _extend_msg(msg):
        try:
            trace_id = LOG_THREAD_VALUE.trace_id
        except AttributeError:
            trace_id = LOG_THREAD_VALUE.trace_id = uuid.uuid4()
        msg = 'trace_id: {} ,'.format(trace_id) + msg
        return msg

    def debug(self, msg, *args, **kwargs):
        self.inner_logger.debug(self._extend_msg(msg), *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.inner_logger.info(self._extend_msg(msg), *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.inner_logger.warning(self._extend_msg(msg), *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        self.inner_logger.warn(self._extend_msg(msg), *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.inner_logger.error(self._extend_msg(msg), *args, **kwargs)

    def exception(self, msg, *args, exc_info=True, **kwargs):
        self.inner_logger.exception(self._extend_msg(msg), *args, exc_info=exc_info, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.inner_logger.critical(self._extend_msg(msg), *args, **kwargs)
