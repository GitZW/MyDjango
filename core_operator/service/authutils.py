# -*- coding: utf-8 -*# -*- coding: utf-8 -*-
from django.middleware.csrf import rotate_token
from django.utils.crypto import constant_time_compare
from core_operator.models import MOperator

SESSION_KEY = '_auth_user_id'
HASH_SESSION_KEY = '_auth_user_hash'
REDIRECT_FIELD_NAME = 'next'
LANGUAGE_SESSION_KEY = '_language'


def login(request, user):
    """
    控制台登录,用到django session,登录要写入session
    不直接使用django.contrib.auth.login方法(会用到不必要的逻辑和model),重写一套简单的
    """
    session_auth_hash = ''
    if user is None:
        user = request.user
    if hasattr(user, 'get_session_auth_hash'):
        session_auth_hash = user.get_session_auth_hash()

    if SESSION_KEY in request.session:
        if get_user_session_key(request) != user.pk or (
                session_auth_hash and
                not constant_time_compare(request.session.get(HASH_SESSION_KEY, ''), session_auth_hash)):
            # To avoid reusing another user's session, create a new, empty
            # session if the existing session corresponds to a different
            # authenticated user.
            request.session.flush()
    else:
        request.session.cycle_key()

    request.session[SESSION_KEY] = user._meta.pk.value_to_string(user)
    request.session[HASH_SESSION_KEY] = session_auth_hash
    if hasattr(request, 'user'):
        request.user = user
    rotate_token(request)


def get_user_session_key(request):
    """
    根据request.session[SESSION_KEY]获取user_id
    """
    return MOperator._meta.pk.to_python(request.session[SESSION_KEY])


def logout(request):
    """
    控制台登出,清除session
    """
    # remember language choice saved to session
    language = request.session.get(LANGUAGE_SESSION_KEY)

    # flush history session
    request.session.flush()

    if language is not None:
        request.session[LANGUAGE_SESSION_KEY] = language

    if hasattr(request, 'user'):
        request.user = get_anonymous_user()


def get_anonymous_user():
    return MOperator(id=None, username=None)
