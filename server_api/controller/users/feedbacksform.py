# -*- coding: utf-8 -*

from django import forms

from utils.common.forms import PaginationForm


class GetFeedbacksForm(PaginationForm):
    load_before = forms.IntegerField(required=False)
    load_after = forms.IntegerField(required=False)


class PostFeedbacksForm(forms.Form):
    content = forms.CharField()
