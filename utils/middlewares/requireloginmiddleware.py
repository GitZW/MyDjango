# -*- coding: utf-8 -*-

from utils import logging
import datetime

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import JsonResponse

from utils.common.exceptions import APIException
from utils.common import errorcode
from utils.common.base import JsonEncoder

logger = logging.getLogger(__name__)
REQUIRE_LOGIN_EXCLUDES = settings.REQUIRE_LOGIN_EXCLUDES if hasattr(settings, 'REQUIRE_LOGIN_EXCLUDES') else []
require_login_excludes = [reverse(url_name) for url_name in REQUIRE_LOGIN_EXCLUDES]


class RequireLoginMiddleware:
    def process_view(self, request, view_func, view_args, view_kwargs):

        if request.path not in require_login_excludes:
            #  自动拦截所有控制台未登陆的请求, REQUIRE_LOGIN_EXCLUDES的除外
            if request.user.id is None:
                return JsonResponse(throws_api_exception(APIException(errorcode.CONSOLE_LOGIN_REQUIRED)),
                                    encoder=JsonEncoder)


def throws_api_exception(exception):
    response = dict(
        status=exception.status,
        # 如果返回类型为ErrorDict(forms.errors), 将其转化为str.
        message=exception.msg,
        timestamp=datetime.datetime.now(),
    )
    return response
