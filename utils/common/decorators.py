from functools import wraps
from importlib import import_module
from inspect import isfunction

from django.http import HttpRequest
from django.views.generic import View

from utils.common import errorcode
from .exceptions import APIException


def require_login(func):
    """修饰一个view, 限制只有登录用户能访问."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        request = args[0]
        assert isinstance(request, HttpRequest)
        if not hasattr(request, 'user_dict') or not request.user_dict:
            # 如果携带token
            if request.META.get('HTTP_X_AUTH_TOKEN'):
                raise APIException(errorcode.LOGIN_TOKEN_INVALID)
            else:
                raise APIException(errorcode.API_LOGIN_REQUIRED)
        return func(*args, **kwargs)

    return wrapper


def validate_form(form_class):
    """
    校验表单的decorator

    :param form_class: django.forms.Form的子类
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            request = args[0]
            if not isinstance(request, HttpRequest):
                raise Exception("view的第一个参数必须是request,如果用于class-based view,"
                                "请使用@method_decorator(require_login)")

            form = form_class(request.DATA)
            if not form.is_valid():
                raise APIException(errorcode.INVALID_ARGS, msg=form.errors)

            return func(*args, **kwargs, cleaned_data=form.cleaned_data)

        return wrapper

    return decorator
