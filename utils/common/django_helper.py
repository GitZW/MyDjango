# -*- coding: utf-8 -*-
from functools import wraps
from django.db import close_old_connections


def close_gone_away_connection(func):
    """
    手动清除当前thread_local下的无用connection

    因为Django没有使用connection pool技术, 而是通过CONN_MAX_AGE参数配置每个request中的conn是否重复使用,
    而具体实现通过信号监控request（signals.request_started.connect(close_old_connections))。
    但是在multi_thread环境下, 比如通过executor.submit是没有request环境的, 所以不能触发.
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        close_old_connections()
        return func(*args, **kwargs)

    return wrapper
