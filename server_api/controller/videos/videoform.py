# -*- coding: utf-8 -*

from django import forms
from django.core.exceptions import ValidationError
from utils.common.forms import PaginationForm


class VideoListForm(PaginationForm):
    category_id = forms.IntegerField(required=False)
