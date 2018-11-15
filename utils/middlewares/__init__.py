# -*- coding: utf-8 -*-
import threading


# 线程本地变量, 贯穿整个请求, 用来保存该线程上下文中需要保持追踪的数据
REQUEST_THREAD_LOCAL = threading.local()
