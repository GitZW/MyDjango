# -*- coding: utf-8 -*-

from django import forms

from utils.common import formfields

MAX_LIMIT = 100


class PaginationForm(forms.Form):
    DEFAULT_OFFSET = 0
    DEFAULT_LIMIT = 10
    offset = forms.IntegerField(required=False, min_value=0)
    limit = forms.IntegerField(required=False, min_value=1)

    def is_valid(self):
        result = super(PaginationForm, self).is_valid()
        if self.cleaned_data.get('offset') is None:
            self.cleaned_data['offset'] = self.DEFAULT_OFFSET
        if self.cleaned_data.get('limit') is None:
            self.cleaned_data['limit'] = self.DEFAULT_LIMIT
        self.cleaned_data['limit'] = min(self.cleaned_data['limit'], MAX_LIMIT)
        return result


class PaginationFormV2(forms.Form):
    DEFAULT_LIMIT = 10
    last_id = forms.IntegerField(required=False, min_value=0)
    limit = forms.IntegerField(required=False, min_value=1)

    def clean_limit(self):
        data = self.cleaned_data['limit']
        if not data:
            data = self.DEFAULT_LIMIT
        self.cleaned_data['limit'] = min(self.cleaned_data['limit'], MAX_LIMIT)
        return data


class PaginationFormV3(PaginationForm):
    cursor = formfields.NoneCharField(required=False)


class BidirectionalPaginationForm(forms.Form):
    cursor = formfields.NoneCharField(required=False)
    mode = formfields.OptionField(required=False, option_values=['down', 'up'])


class UserPaginationFormV3(PaginationFormV3):
    user_id = forms.IntegerField(required=False, min_value=1)


class UserPaginationForm(PaginationForm):
    user_id = forms.IntegerField(required=False, min_value=1)
