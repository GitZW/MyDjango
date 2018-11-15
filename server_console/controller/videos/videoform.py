# -*- coding: utf-8 -*

from django import forms

from utils.common.formfields import BooleanField, ArrayField
from utils.common.forms import PaginationForm


class VideoListForm(PaginationForm):
    category_id = forms.IntegerField(required=False)
    is_free = BooleanField(required=False)
    disable = BooleanField(required=False)


class AddVideoForm(forms.Form):
    title = forms.CharField(max_length=512)
    uri = forms.CharField(max_length=512)
    category_id = ArrayField(base_type=forms.IntegerField(), required=False)
    is_free = BooleanField()
    cover_img = forms.CharField(max_length=512, required=False)
    duration = forms.IntegerField()
    disable = BooleanField()


class UpdateVideoForm(forms.Form):
    title = forms.CharField(max_length=512, required=False)
    uri = forms.CharField(max_length=512, required=False)
    category_id = ArrayField(base_type=forms.IntegerField(), required=False)
    is_free = BooleanField(required=False)
    cover_img = forms.CharField(max_length=512, required=False)
    duration = forms.IntegerField(required=False)
    disable = BooleanField(required=False)
