# -*- coding: utf-8 -*
import datetime

from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST

from core_user.service import userservice
from utils.common.base import JsonEncoder
from utils.common.decorators import validate_form, require_login
from .userform import *


@validate_form(LoginForm)
@require_POST
def login(request, cleaned_data):
    user_dict = userservice.login(**cleaned_data)
    return set_response_cookie(user_dict, cookie_expires=datetime.datetime.now() + datetime.timedelta(days=30))


@validate_form(RegisterForm)
@require_POST
def register(request, cleaned_data):
    user_id = userservice.register(**cleaned_data)

    user_dict = userservice.login(cleaned_data['name'], cleaned_data['pwd'])

    return set_response_cookie(user_dict, cookie_expires=datetime.datetime.now() + datetime.timedelta(days=30))


@require_POST
@require_login
def logout(request):
    user_id = request.user_id
    userservice.delete_user_token(user_id)
    return set_response_cookie(dict(), cookie_expires=datetime.datetime.now())


def set_response_cookie(user_dict=None, cookie_expires=None):
    return_code = dict(
        status=200,
        message="OK",
        timestamp=datetime.datetime.now(),
        data=user_dict
    )

    response = JsonResponse(return_code, encoder=JsonEncoder)
    response.set_cookie('HTTP_X_AUTH_TOKEN', user_dict.get('token'),
                        expires=cookie_expires)
    return response


@require_login
@require_GET
def get_user_info(request):
    user_id = request.user_id
    return userservice.get_user_info(user_id=user_id)
