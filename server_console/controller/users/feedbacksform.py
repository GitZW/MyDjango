# -*- coding: utf-8 -*

from django import forms

from utils.common.forms import PaginationForm
from utils.common.formfields import BooleanField


class GetFeedbacksForm(PaginationForm):
    user_id = forms.IntegerField(required=False)
    is_replied = BooleanField(required=False)
    operator_id = forms.IntegerField(required=False)


class PostFeedbacksForm(forms.Form):
    content = forms.CharField(max_length=1024)


class GetFeedbackHistoryForm(PaginationForm):
    load_before = forms.IntegerField(required=False)
    load_after = forms.IntegerField(required=False)
