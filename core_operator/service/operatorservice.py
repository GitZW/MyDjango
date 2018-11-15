# -*- coding: utf-8 -*
from ..models import MOperator
from core_user.service import userservice
from utils.common.exceptions import APIException
from utils.common import errorcode


def get_operator_list(limit, offset):
    moperators = MOperator.objects.filter(disable=False)
    total = moperators.count()
    return total, [moperator.to_dict() for moperator in moperators[offset:offset + limit]]


def login(username, password):
    moperator = MOperator.objects.filter(username=username, password=userservice.encode_password(password)).first()
    if not moperator:
        raise APIException(errorcode.USER_WRONG_PASSWORD)

    if moperator.disable:
        raise APIException(errorcode.USER_DISABLE)

    return moperator


def check_username_exists(username):
    return MOperator.objects.filter(username=username).exists()


def add_operator(username, password):
    if check_username_exists(username):
        raise APIException(errorcode.USER_NICKNAME_DUPLICATION)
    m = MOperator(username=username, password=userservice.encode_password(password))
    m.save()

    return m.id


def get_operator_info(operator_id):
    moperator = MOperator.objects.get(id=operator_id)
    return moperator.to_dict()


def _get_operator_by_id(operator_id):
    return MOperator.objects.get(id=operator_id)


def get_operator_id_and_name_dict(operator_id, with_name=True):
    if not operator_id:
        return None
    operator = get_operator_info(operator_id)
    if not with_name:
        operator['name'] = "客服"
    return dict(id=operator['id'], name=operator['name'])
