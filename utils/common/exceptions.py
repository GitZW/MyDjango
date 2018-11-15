# -*- coding: utf-8 -*-


class APIException(Exception):
    """
    业务异常类
    """

    def __init__(self, errorcode, msg=None):
        """
        exception的构造函数, 需传入ErrorCode对象, 如果msg不为空, 用传入的msg替换掉errorcode的msg.
        :param errorcode: ErrorCode对象.
        :param msg: 要替换的msg.
        :return:
        """
        self.status = errorcode.id
        self.msg = msg if msg else errorcode.msg
