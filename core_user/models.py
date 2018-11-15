# -*- coding: utf-8 -*

from django.db import models
from core_operator.models import MOperator


class MUser(models.Model):
    name = models.CharField(unique=True, max_length=16)
    pwd = models.CharField(max_length=36)
    is_member = models.BooleanField(default=False)

    member_expire_time = models.DateTimeField(null=True)
    joined_member_time = models.DateTimeField(null=True)
    total_recharge = models.IntegerField(default=0)  # 单位分
    disable = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            is_member=self.is_member,
            member_expire_time=self.member_expire_time,
            joined_member_time=self.joined_member_time,
            total_recharge=self.total_recharge,
            disable=self.disable,
            create_at=self.create_at,
            update_at=self.update_at,
        )


class MUserToken(models.Model):
    user = models.ForeignKey(MUser)
    token = models.CharField(max_length=36, db_index=True)
    delete_flag = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)


class MFeedback(models.Model):
    user = models.OneToOneField(MUser)
    content = models.CharField(max_length=1024)
    is_read = models.BooleanField(default=False)
    is_replied = models.BooleanField(default=False)
    operator = models.ForeignKey(MOperator, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        return dict(
            id=self.id,
            user_id=self.user_id,
            content=self.content,
            is_read=self.is_read,
            is_replied=self.is_replied,
            operator_id=self.operator_id,
            create_at=self.create_at,
            update_at=self.update_at,

        )


class MFeedbackHistory(models.Model):
    user = models.ForeignKey(MUser)
    content = models.CharField(max_length=1024)
    operator = models.ForeignKey(MOperator, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        return dict(
            id=self.id,
            user_id=self.user_id,
            content=self.content,
            operator_id=self.operator_id,
            create_at=self.create_at,
            update_at=self.update_at,
        )


class MUserLike(models.Model):
    user = models.ForeignKey(MUser)
    target_id = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "target_id")
