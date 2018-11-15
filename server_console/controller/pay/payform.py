# -*- coding: utf-8 -*

from django import forms
from django.core.exceptions import ValidationError
from utils.common.forms import PaginationForm


class AddPaywayForm(forms.Form):
    title = forms.CharField(max_length=512)
    img = forms.CharField(max_length=512)
    desc = forms.CharField(max_length=512)


class UpdatePaywayForm(forms.Form):
    title = forms.CharField(max_length=512, required=False)
    img = forms.CharField(max_length=512, required=False)
    desc = forms.CharField(max_length=512, required=False)
