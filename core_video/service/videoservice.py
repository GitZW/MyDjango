# -*- coding: utf-8 -*-
import random
import logging
from ..models import MCategory, MVideo, MVideoCategory
from core_user.models import MUserLike
from utils.common import gf_conf
from django.db.models import F
from django.db import transaction

logger = logging.getLogger(__name__)


def get_video_list(category_id=None, is_free=None, disable=None, limit=10, offset=0):
    logger.info("get_video_list {} {}".format(category_id, is_free))
    mvideo_set = MVideo.objects.filter(delete_flag=False).order_by('-id')
    if category_id:
        video_ids = get_video_ids_by_category_id(category_id)
        mvideo_set = mvideo_set.filter(id__in=video_ids)

    if is_free is not None:
        mvideo_set = mvideo_set.filter(is_free=is_free)

    if disable is not None:
        mvideo_set = mvideo_set.filter(disable=disable)

    total = mvideo_set.count()
    return total, [video.to_dict() for video in mvideo_set[offset:offset + limit]]


def get_video_ids_by_category_id(category_id):
    return MVideoCategory.objects.filter(category_id=category_id).values_list('video_id', flat=True)


def get_category_dict():
    category_id_name_dict = dict()
    for m in MCategory.objects.all():
        category_id_name_dict[m.id] = m.to_dict()

    return category_id_name_dict


def get_categories():
    return [m.to_dict() for m in MCategory.objects.all().order_by('-weight', 'id')]


def get_video_by_id(video_id):
    mvideo = _get_video_by_id(video_id)
    increase_video_play_count(video_id, random.randint(1, 5))

    return mvideo.to_dict()


def _get_video_by_id(video_id):
    return MVideo.objects.get(id=video_id)


def add_video(title, category_id, uri, duration, is_free, uploader_id, cover_img=None, disable=None):
    """
    :return:
    """
    logging.info(
        "add video {} {} {} {} {} {} {}".format(title, category_id, uri, cover_img, duration, is_free, uploader_id))
    with transaction.atomic():

        mvideo = MVideo(title=title, uri=uri, cover_img=cover_img, duration=duration,
                        is_free=is_free, uploader_id=uploader_id, category=category_id)

        if disable is not None:
            mvideo.disable = disable
        mvideo.save()

        for cat_id in category_id:
            MVideoCategory.objects.create(video=mvideo, category_id=cat_id)

    return mvideo.id


def delete_video(video_id):
    mvideo = MVideo.objects.get(id=video_id)
    mvideo.delete_flag = True
    mvideo.save(update_fields=['delete_flag'])


def update_video(video_id, title=None, category_id=None, uri=None, cover_img=None, duration=None, is_free=None,
                 disable=None):
    mvideo = MVideo.objects.get(id=video_id)
    if title:
        mvideo.title = title
    if category_id:
        mvideo.category_id = category_id
    if uri:
        mvideo.uri = uri
    if cover_img:
        mvideo.cover_img = cover_img
    if duration:
        mvideo.duration = duration
    if is_free is not None:
        mvideo.is_free = is_free
    if disable is not None:
        mvideo.disable = disable
    if category_id:
        mvideo.category = category_id
        MVideoCategory.objects.filter(video_id=video_id).delete()

        for cat_id in category_id:
            MVideoCategory.objects.create(video_id=mvideo.id, category_id=cat_id)

    mvideo.save()


def add_like(user_id, video_id):
    m = MUserLike(user_id=user_id, target_id=video_id)
    m.save()
    increase_video_like_count(video_id, random.randint(1, 3))


def has_liked(user_id, video_id):
    return MUserLike.objects.filter(user_id=user_id, target_id=video_id).exists()


def increase_video_like_count(video_id, count=1):
    MVideo.objects.filter(id=video_id).update(like_count=F('like_count') + count)


def increase_video_play_count(video_id, count=1):
    MVideo.objects.filter(id=video_id).update(play_count=F('play_count') + count)


def get_resource_domain():
    domains = gf_conf.get_value("app_domain")
    if not isinstance(domains, list):
        domains = [domains]
    return random.choice(domains)
