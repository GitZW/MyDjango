# -*- coding: utf-8 -*
import re
import logging
from datetime import timedelta, datetime
from uuid import uuid4
from hashlib import md5
from ..models import MUser, MUserToken
from utils.common.exceptions import APIException
from utils.common import errorcode
from core_pay.service.payservice import PayType
from django.db import transaction
from core_order.service.orderservice import DurationType

logger = logging.getLogger(__name__)
_SALT = "@#3%2$&"


def encode_password(passwd):
    return md5((passwd + _SALT).encode('utf-8')).hexdigest()


def check_password_chars(user_password):
    try:
        user_password.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


def check_user_name_chars(user_name):
    m = re.match(r'^[0-9a-zA-Z\u4e00-\u9fa5]{1,50}$', user_name)
    if m is None:
        return False
    return True


def login(name, pwd):
    pwd = encode_password(pwd)
    m_user = MUser.objects.filter(name=name, pwd=pwd).first()
    if not m_user:
        raise APIException(errorcode.USER_WRONG_PASSWORD)
    user_dict = m_user.to_dict()
    if user_dict['disable']:
        raise APIException(errorcode.USER_WRONG_PASSWORD)

    delete_user_token(user_dict['id'])
    m_token = MUserToken.objects.create(user_id=user_dict['id'], token=str(uuid4()))

    user_dict['token'] = m_token.token

    return user_dict


def delete_user_token(user_id):
    MUserToken.objects.filter(user_id=user_id).delete()


def check_username_exists(name):
    return MUser.objects.filter(name=name).exists()


def register(name, pwd, pwd_again):
    assert name
    assert pwd
    assert pwd_again
    if pwd != pwd_again:
        raise APIException(errorcode.USER_DIFF_PWD_AGAIN)
    if not check_password_chars(pwd_again):
        raise APIException(errorcode.USER_PASSWORD_INVALID_WORD)
    if check_username_exists(name):
        raise APIException(errorcode.USER_NICKNAME_DUPLICATION)

    muser = MUser(name=name, pwd=encode_password(pwd))
    muser.save()
    return muser.id


def get_user_info(user_id=None, name=None):
    assert user_id or name
    muser_set = MUser.objects.all()
    if user_id:
        muser_set = muser_set.filter(id=user_id)
    if name:
        muser_set = muser_set.filter(name=name)

    if not muser_set:
        raise APIException(errorcode.USER_DONT_EXISTS)
    return muser_set.first().to_dict()


def get_user_by_token(token):
    """根据登录token获取用户信息, 不存在不抛异常"""
    user_token = MUserToken.objects.filter(token=token).first()
    if user_token:
        return user_token.user.to_dict()

    return None


def get_user_list(user_id=None, is_member=None, name=None, order_by=None, limit=20, offset=0):
    musers = MUser.objects.all()
    if user_id:
        musers = musers.filter(id=user_id)
    if is_member is not None:
        musers = musers.filter(is_member=is_member)
    if name:
        musers = musers.filter(name=name)

    musers = musers.order_by('-id')
    total = musers.count()

    return total, [muser.to_dict() for muser in musers[offset:limit + offset]]


def _get_user_by_id(user_id, lock=False):
    if lock:
        muser = MUser.objects.filter(pk=user_id).select_for_update().first()
    else:
        muser = MUser.objects.filter(pk=user_id).first()

    if not muser:
        raise APIException(errorcode.USER_DONT_EXISTS)
    return muser


def get_user_id_and_name(user_id):
    if not user_id:
        return None
    user = _get_user_by_id(user_id)
    return dict(id=user.id, name=user.name)


def add_user_member_expire_time(operator_id, user_id, amount, duration, duration_type):
    assert operator_id
    assert user_id
    assert duration
    assert isinstance(duration_type, DurationType)

    logger.info("add_user_member_expire_time {} {} {} {} {}".format(operator_id, user_id, amount, duration,
                                                                    duration_type.value))
    with transaction.atomic():
        muser = _get_user_by_id(user_id, lock=True)
        now = datetime.now()
        if duration_type == DurationType.D:
            duration = timedelta(days=duration)
        elif duration_type == DurationType.M:
            duration = timedelta(days=duration * 31)
        else:
            duration = timedelta(days=duration * 366)

        if not muser.joined_member_time:
            muser.joined_member_time = now

        current_expire_time = muser.member_expire_time
        if not current_expire_time or current_expire_time < now:
            muser.member_expire_time = now + duration
        else:
            muser.member_expire_time += duration

        muser.is_member = True
        muser.total_recharge += amount
        muser.save()

    logging.info("user member time change {} --> {}".format(current_expire_time, muser.member_expire_time))
    return current_expire_time, muser.member_expire_time


def check_user_member_status():
    for muser in MUser.objects.filter(is_member=True, member_expire_time__lt=datetime.now()):
        muser.is_member = False
        muser.save(update_fields=['is_member'])
