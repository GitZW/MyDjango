# -*- coding: utf-8 -*

from django.views.generic import View
from django.views.decorators.http import require_GET, require_POST

from utils.common.decorators import validate_form, require_login
from django.utils.decorators import method_decorator
from core_order.service import orderservice
from core_user.service import userservice
from core_operator.service import operatorservice
from .orderform import *


class OrderList(View):
    @method_decorator(validate_form(OrderListForm))
    def get(self, request, cleaned_data):
        total, orders = orderservice.get_order_list(**cleaned_data)
        return dict(total=total, orders=wrap_order(orders))

    @method_decorator(validate_form(AddOrderForm))
    def post(self, request, cleaned_data):
        operator_id = request.user.id
        order_id = orderservice.add_order(operator_id, **cleaned_data)
        return dict(id=order_id)


def wrap_order(orders):
    result = []
    for order in orders:
        order['user'] = userservice.get_user_id_and_name(order['user_id'])
        order['operator'] = operatorservice.get_operator_id_and_name_dict(order['operator_id'])

        result.append(order)

    return result
