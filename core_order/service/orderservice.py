# -*- coding: utf-8 -*
import enum
import logging
from django.db import transaction
from core_order.models import MOrder
from core_pay.service.payservice import PayType
from core_user.service import userservice

logger = logging.getLogger(__name__)


class DurationType(enum.Enum):
    D = 'd'  # 日
    M = 'm'  # 月
    Y = 'y'  # 年


def add_order(operator_id, user_id, amount, out_trans_no, pay_type, duration, duration_type, desc=None):
    assert isinstance(pay_type, PayType)
    assert amount > 0
    assert out_trans_no
    assert duration > 0
    assert isinstance(duration_type, DurationType)

    logger.info(
        "add_order {} {} {} {} {} {} {} {}".format(operator_id, user_id, amount, out_trans_no, pay_type.value, duration,
                                                   duration_type.value, desc))

    with transaction.atomic():
        current_expire_time, member_expire_time = userservice.add_user_member_expire_time(operator_id, user_id, amount,
                                                                                          duration, duration_type)
        morder = MOrder(user_id=user_id, operator_id=operator_id, amount=amount, out_trans_no=out_trans_no,
                        pay_type=pay_type.value, duration=duration, current_expire_time=current_expire_time,
                        member_expire_time=member_expire_time, duration_type=duration_type.value, desc=desc)

        morder.save()

    return morder.id


def get_order_list(user_id=None, pay_type=None, order_by=None, limit=10, offset=0):
    morders = MOrder.objects.all()
    total = morders.count()
    if user_id:
        morders = morders.filter(user_id=user_id)
    if pay_type:
        morders = morders.filter(pay_type=pay_type.value)

    morders.order_by('-create_at')
    return total, [morder.to_dict() for morder in morders[offset:offset + limit]]
