# -*- coding: utf-8 -*-

import datetime
from django.conf import settings
from django.http import JsonResponse
from utils.common import errorcode
from utils.common.base import JsonEncoder


class BlackIPlistMiddleware:
    """
    ip黑名单拦截
    """

    def process_request(self, request):
        black_ips = []
        for blk_ip in black_ips:
            if request.ip.startswith(blk_ip):
                response = dict(
                    status=errorcode.IP_LIMITED.id,
                    message=errorcode.IP_LIMITED.msg,
                    timestamp=datetime.datetime.now(),
                )
                return JsonResponse(response, encoder=JsonEncoder)
