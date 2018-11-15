# -*- coding: utf-8 -*-
import json
from django.conf import settings
from utils import logging
import datetime
import re
from xml.dom import minidom
from django.forms.utils import ErrorDict
from django.http import JsonResponse, QueryDict, HttpResponse
from django.utils.datastructures import MultiValueDict
from utils.common.exceptions import APIException
from utils.common.base import JsonEncoder
from utils.common import errorcode
logger = logging.getLogger(__name__)


class APIMiddleware:
    """APIMiddleware, 为更方便的设计和实现API而生.

    该Middleware允许view返回dict类型, 最好放在MIDDLEWARE_CLASSES的最后.

    该middleware做了以下事情:
    拦截所有request进入, 并把url参数和body里面的参数封装到request.DATA.
    拦截所有APIException, 并封装好错误错误信息给接口调用者.
    拦截view返回的所有dict类型数据, 并封装成
    平台要求的数据格式,以JSONResponse返回给接口调用者.
    """
    # def __init__(self, get_response):
    #     self.get_response = get_response
    #     # One-time configuration and initialization.
    #
    # def __call__(self, request):
    #     # Code to be executed for each request before
    #     # the view (and later middleware) are called.
    #
    #     response = self.get_response(request)
    #
    #     # Code to be executed for each request/response after
    #     # the view is called.
    #
    #     return response

    # 匹配[]的正则表达式,只在第一次编译
    match = re.compile(r'%5[Bb]\d*%5[Dd](?==)')

    def process_request(self, request):
        """
        拦截进入的所有request,为每个request编号;拦截所有request进入, 把request_id和ip,device,data等信息打印到log
        拦截所有request进入, 并把url参数和body里面的参数封装到request.DATA.
        """
        if settings.global_reject_service if hasattr(settings, 'global_reject_service') else False:
            # 服务升级中, 所有接口不可用
            response = dict(
                status=609,
                # 如果返回类型为ErrorDict(forms.errors), 将其转化为str.
                message='服务正在升级,请稍候重试!',
                timestamp=datetime.datetime.now(),
            )
            return JsonResponse(response, encoder=JsonEncoder)

        # 生成request.DATA
        request.DATA = QueryDict('')
        request.QUERY_DATA = QueryDict(request.META['QUERY_STRING'])
        if request.method == 'GET':
            body = request.META['QUERY_STRING']
        else:
            body = request.body.decode()

        if request.META.get('CONTENT_TYPE', '').startswith('multipart'):
            request.DATA, request._files = request.parse_file_upload(request.META, request)
        else:
            dict_body = self.match.sub('', body)  # 删除所有"="前的"%5B%5D"([]的转义)
            request.DATA, request._files = QueryDict(dict_body), MultiValueDict()

        if request.META.get('CONTENT_TYPE', '').startswith('application/json'):
            try:
                request.JSON_DATA = json.loads(body)
            except:
                logger.info('process json fail: {}'.format(request.META.get('CONTENT_TYPE', '')))
        elif 'xml' in request.META.get('CONTENT_TYPE', ''):
            try:
                request.XML_DATA = minidom.parseString(body)
            except:
                logger.info('process xml fail: {}'.format(request.META.get('CONTENT_TYPE', '')))

        # 封装api version
        request.version = request.META.get('HTTP_X_API_VERSION')
        request.token = request.META.get('HTTP_X_AUTH_TOKEN')

    def process_exception(self, request, exception):
        if isinstance(exception, APIException):
            response = dict(
                status=exception.status,
                # 如果返回类型为ErrorDict(forms.errors), 将其转化为str.
                message=exception.msg if not isinstance(exception.msg, ErrorDict) else exception.msg.as_text(),
                timestamp=datetime.datetime.now(),
            )
            logger.info("{method} {api_url}, APIException: status={status} msg={msg}".format(
                method=request.method.upper(), api_url=request.path,
                status=exception.status, msg=exception.msg))
            return JsonResponse(response, encoder=JsonEncoder)

    def process_response(self, request, response):
        if isinstance(response, dict) or isinstance(response, list):
            wrap_data = dict(
                status=200,
                message="OK",
                timestamp=datetime.datetime.now(),
            )
            wrap_data['data'] = response
            return JsonResponse(wrap_data, encoder=JsonEncoder)
        elif isinstance(response, str):
            return HttpResponse(response)
        elif response is None:
            return HttpResponse('')
        else:
            return response
