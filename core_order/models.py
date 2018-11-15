# -*- coding: utf-8 -*

from django.db import models
from core_user.models import MUser
from core_operator.models import MOperator

"""
# class MOrder:
#     user
#     amount
#     pay_type = wx|al
#     out_trans_no = ''
#     duration = 6
#     duration_type = d|m|y
#     expire_time =
"""


class MOrder(models.Model):
    user = models.ForeignKey(MUser)
    operator = models.ForeignKey(MOperator)
    amount = models.IntegerField()  # 单位分
    pay_type = models.CharField(max_length=32)
    out_trans_no = models.CharField(max_length=128, unique=True)
    duration = models.IntegerField()
    duration_type = models.CharField(max_length=16)
    desc = models.CharField(max_length=512, null=True)  # 备注

    # 冗余，充值前后会员的时间
    current_expire_time = models.DateTimeField(null=True)
    member_expire_time = models.DateTimeField(null=True)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        return dict(
            id=self.id,
            user_id=self.user_id,
            operator_id=self.operator_id,
            amount=self.amount,
            pay_type=self.pay_type,
            out_trans_no=self.out_trans_no,
            duration=self.duration,
            duration_type=self.duration_type,
            desc=self.desc,
            create_at=self.create_at,
            update_at=self.update_at,
        )
