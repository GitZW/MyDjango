# -*- coding: utf-8 -*

from django.views.decorators.http import require_GET, require_POST

from core_pay.service import payservice
from utils.common.decorators import validate_form, require_login
from utils.domainutils import *


@require_GET
def get_pay_ways(request):
    pay_ways = payservice.get_pay_ways()
    return dict(pay_ways=wrap_pay_ways(pay_ways))


def wrap_pay_ways(pay_ways):
    result = []
    for pay in pay_ways:
        pay['full_img'] = full_domain(pay['img'] + '.jpg', with_token=False)
        result.append(pay)

    return result


@require_GET
def get_price(request):
    list_price = [
        {
            "name": "月套餐",
            "price": "38"
        },
        {
            "name": "季套餐（8.5折）",
            "price": "98"
        },
        {
            "name": "半年套餐（6折）",
            "price": "138"
        }
    ]
    return dict(pay_price=list_price)
