# -*- coding: utf-8 -*

from django import forms
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    name = forms.CharField(required=True, min_length=4, max_length=16)
    pwd = forms.CharField(required=True, min_length=6, max_length=16)


class RegisterForm(forms.Form):
    name = forms.CharField(required=True, min_length=4, max_length=16)
    pwd = forms.CharField(required=True, min_length=6, max_length=16)
    pwd_again = forms.CharField(required=True, min_length=6, max_length=16)
