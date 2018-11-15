# -*- coding: utf-8 -*
from django.db import models
from core_operator.models import MOperator
from utils.common.custommodelfields import ListField


class MCategory(models.Model):
    name = models.CharField(max_length=64)
    weight = models.IntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            weight=self.weight
        )


class MVideo(models.Model):
    title = models.CharField(max_length=1024)
    category = ListField(base_type=int, max_length=128, null=True)
    uri = models.CharField(unique=True, max_length=128)

    cover_img = models.CharField(max_length=128, null=True)
    duration = models.IntegerField()
    is_free = models.BooleanField(default=False)
    play_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    uploader = models.ForeignKey(MOperator)
    delete_flag = models.BooleanField(default=False)
    disable = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        return dict(
            id=self.id,
            title=self.title,
            uri=self.uri,
            cover_img=self.cover_img,
            duration=self.duration,
            is_free=self.is_free,
            play_count=self.play_count,
            like_count=self.like_count,
            delete_flag=self.delete_flag,
            uploader_id=self.uploader_id,
            category_id=self.category or [],
            disable=self.disable
        )


class MVideoCategory(models.Model):
    video = models.ForeignKey(MVideo)
    category = models.ForeignKey(MCategory)
