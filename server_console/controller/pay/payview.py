# -*- coding: utf-8 -*

from django.views.decorators.http import require_GET, require_POST
from django.utils.decorators import method_decorator

from core_pay.service import payservice
from utils.common.decorators import validate_form, require_login
from utils.domainutils import *
from django.views.generic import View
from utils.common.forms import PaginationForm
from .payform import AddPaywayForm, UpdatePaywayForm


class PaywaysView(View):
    def get(self, request):
        pay_ways = payservice.get_pay_ways()
        return dict(pay_ways=wrap_pay_way(pay_ways))

    @method_decorator(validate_form(AddPaywayForm))
    def post(self, requset, cleaned_data):
        pay_id = payservice.add_pay_way(**cleaned_data)
        return dict(id=pay_id)


class PaywaysDetailView(View):
    def get(self, request, way_id):
        pay_way = payservice.get_pay_way_by_id(way_id)
        return wrap_pay_way(pay_way)

    @method_decorator(validate_form(UpdatePaywayForm))
    def put(self, requset, way_id, cleaned_data):
        payservice.update_pay_way(way_id, **cleaned_data)
        return dict(id=1)

    def delete(self, request, way_id):
        payservice.delete_pay_way(way_id)

        return dict(id=1)


def wrap_pay_way(pay_way):
    result = []
    if not isinstance(pay_way, list):
        pay_way = [pay_way]
    for way in pay_way:
        way['img'] = full_domain(way['img'] + '.jpg', with_token=False)
        result.append(way)

    return result
