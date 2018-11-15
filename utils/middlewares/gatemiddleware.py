# -*- coding: utf-8 -*-

import datetime
import traceback
import uuid

from django.conf import settings
from django.utils.cache import patch_vary_headers

from utils import logging

logger = logging.getLogger(__name__)


class ApiGateMiddleware:
    """GateMiddleware

    Gate,大门,所有API访问的进出口.
    该middleware应该放在middlewares的第一位

    该middleware做了以下事情:
    为每个request编号;
    拦截所有request进入, 把trace_id和ip,device,data等信息打印到log;
    拦截所有request出去, 把trace_id和此次访问所耗时间打印到log;
    """

    def process_request(self, request):

        # 记录request进入的时间, 为request编号
        request.incoming_time = datetime.datetime.now()

        request.ip = get_client_ip(request)
        request.device = request.META.get('HTTP_USER_AGENT')

        logging.clear_trace()

        # 标识来自浏览器的请求
        web_trace_id = request.COOKIES.get('__web_trace_id', None)
        if web_trace_id:
            request.web_trace_id = web_trace_id
        else:
            request.web_trace_id = uuid.uuid4().hex

    def process_view(self, request, view_func, view_args, view_kwargs):
        """打印request进入时的log"""
        user = request.user_dict and '%s(%s)' % (request.user_dict.get('id'), request.user_dict.get('name'))
        logger.info("{method}:{api_version} {api_url}, USER: {user}, DATA: {data}, IP: {ip}, "
                    "DEVICE: {device}".format(user=user, method=request.method.upper(), api_url=request.path,
                                              api_version=request.META.get('HTTP_X_API_VERSION') or '',
                                              data={k: str(v)[:1000] for k, v in dict(request.DATA).items()},
                                              ip=request.ip, device=request.device))

    def process_response(self, request, response):
        """拦截所有request出去, 把trace_id和此次访问所耗时间打印到log"""
        if request.method.upper() == 'OPTIONS':
            return response

        duration = int((datetime.datetime.now() - request.incoming_time).total_seconds() * 1000)
        logger.info("URL: {method}:{api_version} {api_url}, Duration:{duration}".format(
            method=request.method.upper(), api_version=request.META.get('HTTP_X_API_VERSION') or '',
            api_url=request.path, duration=duration))
        # 对慢请求做出错报警
        if duration >= 6000:
            logger.warn("slow request, url: {api_url}, duration:{duration}".format(
                api_url=request.path, duration=duration))

        # 如果来自浏览器请求, 则添加cookie用于记录访问设备
        patch_vary_headers(response, ('Cookie',))
        if not request.COOKIES.get('__web_trace_id', None):
            response.set_cookie('__web_trace_id', request.web_trace_id,
                                path=settings.SESSION_COOKIE_PATH, secure=settings.SESSION_COOKIE_SECURE or None,
                                httponly=settings.SESSION_COOKIE_HTTPONLY or None,
                                domain=settings.SESSION_COOKIE_DOMAIN, max_age=30 * 24 * 3600)

        return response

    def process_exception(self, request, exception):
        """拦截所有未处理的exception,并把traceback转化为一行数据打印到log"""
        user_repr = "{user_id}({nickname}, {phone})".format(user_id=request.user_dict.get('id'),
                                                            nickname=request.user_dict.get('nickname'),
                                                            phone=request.user_dict.get('phone'))
        logger.error(
            'REQUEST URL: %s, USER: %s, Unexpected Exception: %s' % (
                request.path, user_repr, traceback.format_exc()))


class ConsoleGateMiddleware:
    # 匹配[]的正则表达式,只在第一次编译

    def process_request(self, request):
        """
        拦截进入的所有request,为每个request编号;拦截所有request进入, 把trace_id和ip,device,data等信息打印到log
        拦截所有request进入, 并把url参数和body里面的参数封装到request.DATA.
        """
        logging.clear_trace()

        # 打印request进入时的log
        request.incoming_time = datetime.datetime.now()

        request.ip = get_client_ip(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        """打印request进入时的log"""
        user = '%s(%s)' % (request.user.id, request.user.username) if request.user.id is not None else None
        logger.info("{method}: {api_url}, USER: {user}, DATA: {data}, IP: {ip}".format(
            api_url=request.path, method=request.method.upper(), user=user,
            data=dict(request.DATA), ip=request.ip))

    def process_response(self, request, response):
        """拦截所有request出去, 把trace_id和此次访问所耗时间打印到log"""
        logger.info("Duration:{duration}".format(
            duration=int((datetime.datetime.now() - request.incoming_time).total_seconds() * 1000)))
        return response

    def process_exception(self, request, exception):
        """拦截所有未处理的exception,并把traceback转化为一行数据打印到log"""
        logger.error('Unexpected Exception: \n%s' % traceback.format_exc())


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
