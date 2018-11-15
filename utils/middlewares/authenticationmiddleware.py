# -*- coding: utf-8 -*-

from django.conf import settings
# from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject

from core_operator.service.authutils import *
from core_user.service.userservice import get_user_by_token
from core_operator.models import MOperator
from core_operator.service.operatorservice import _get_operator_by_id


class AuthenticationMiddleware:

    def process_request(self, request):
        """
        拦截request, 并封装user_dict到request
        """
        request.user_dict = {}
        request.user_id = None
        token = request.COOKIES.get('HTTP_X_AUTH_TOKEN')  # token被django转换成HTTP_TOKEN存放在META里面.
        # user_dict = request.META.get('HTTP_X_AUTH_TOKEN')  # token被django转换成HTTP_TOKEN存放在META里面.

        if token:
            user_dict = get_user_by_token(token)
            request.user_dict = user_dict if user_dict else {}
            request.user_id = user_dict and user_dict['id']


def get_user(request):
    def _get_user(request):
        try:
            user_id = get_user_session_key(request)
        except KeyError:
            user = None
        else:
            try:
                user = MOperator.objects.get(id=user_id)
            except MOperator.DoesNotExist:
                user = None
        return user or get_anonymous_user()

    if not hasattr(request, '_cached_user'):
        request._cached_user = _get_user(request)
    return request._cached_user


class ConsoleAuthenticationMiddleware:
    """
    控制台authentication,封装request.user对象
    """

    def process_request(self, request):
        assert hasattr(request, 'session'), (
                                                "The authentication middleware requires session middleware "
                                                "to be installed. Edit your MIDDLEWARE%s setting to insert "
                                                "'django.contrib.sessions.middleware.SessionMiddleware' before "
                                                "'utils.middlewares.authenticationmiddleware.ConsoleAuthenticationMiddleware'."
                                            ) % ("_CLASSES" if settings.MIDDLEWARE is None else "")
        request.user = SimpleLazyObject(lambda: get_user(request))
