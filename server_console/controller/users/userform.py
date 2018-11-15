# -*- coding: utf-8 -*

from django import forms

from utils.common.formfields import OptionField, BooleanField
from utils.common.forms import PaginationForm


class UserListForm(PaginationForm):
    user_id = forms.IntegerField(required=False)
    is_member = BooleanField(required=False)
    name = forms.CharField(required=False)
    order_by = OptionField(option_values=['create_at', '-create_at'], required=False)
