# -*- coding: utf-8 -*

from django.views.decorators.http import require_GET, require_POST

from core_operator.service import operatorservice, authutils
from utils.common.decorators import validate_form
from utils.common.forms import PaginationForm
from .operatorsform import LoginForm, RegisterForm


@require_GET
@validate_form(PaginationForm)
def get_operator_list(request, cleaned_data):
    total, operators = operatorservice.get_operator_list(**cleaned_data)
    return dict(operators=operators, total=total)


@require_POST
@validate_form(LoginForm)
def login(request, cleaned_data):
    username = cleaned_data.get('username')
    password = cleaned_data.get('password')
    user = operatorservice.login(username, password)

    authutils.login(request, user)

    return dict(user=user.to_dict())


@require_POST
@validate_form(RegisterForm)
def register(request, cleaned_data):
    username = cleaned_data.get('username')
    password = cleaned_data.get('password')
    operator_id = operatorservice.add_operator(username, password)
    return dict(id=operator_id)
