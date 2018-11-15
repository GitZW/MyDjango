# -*- coding: utf-8 -*

from django import forms
from django.core.exceptions import ValidationError

from django import forms
from django.core.exceptions import ValidationError
from utils.common.forms import PaginationForm
from utils.common.formfields import OptionField, EnumField
from core_pay.service.payservice import PayType
from core_order.service.orderservice import DurationType


class OrderListForm(PaginationForm):
    user_id = forms.IntegerField(required=False)
    pay_type = EnumField(base_type=PayType, required=False)
    order_by = OptionField(option_values=['create_at', '-create_at'], required=False)


class AddOrderForm(forms.Form):
    user_id = forms.IntegerField()
    amount = forms.IntegerField()
    pay_type = EnumField(base_type=PayType)
    out_trans_no = forms.CharField(max_length=64)
    duration = forms.IntegerField()
    duration_type = EnumField(base_type=DurationType)
    desc = forms.CharField(max_length=512, required=False)
