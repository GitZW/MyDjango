# -*- coding: utf-8 -*

from django.views.decorators.http import require_GET, require_POST

from core_video.service import videoservice
from utils.common.decorators import validate_form, require_login
from .videoform import *
from utils.domainutils import *
from core_user.service import userservice
from django.views.generic import View


@require_GET
@validate_form(VideoListForm)
def get_videos(request, cleaned_data):
    user_id = request.user_id
    _, videos = videoservice.get_video_list(**cleaned_data, disable=False)
    return dict(videos=[wrap_videos(user_id, video) for video in videos])


class VideoDetail(View):
    def get(self, request, video_id):
        user_id = request.user_id
        video = videoservice.get_video_by_id(int(video_id))
        return wrap_videos(user_id, video)


@require_GET
def get_video_categories(reuqest):
    categories = videoservice.get_categories()
    categories = [wrap_category(category) for category in categories]
    return categories


@require_login
@require_POST
def add_like(request, video_id):
    user_id = request.user_id
    videoservice.add_like(user_id, video_id)
    return dict()


def wrap_category(category_dict):
    r = dict(id=category_dict['id'], name=category_dict['name'])

    return r


def wrap_videos(user_id, video):
    """
    :param user_id:
    :param videos:
    :return:
    """
    category_dict = videoservice.get_category_dict()
    user_dict = {}
    if user_id:
        user_dict = userservice.get_user_info(user_id=user_id)
    if video['is_free']:
        can_play_all = True

    else:
        can_play_all = user_dict['is_member'] if user_dict else False
    video['category'] = [category_dict.get(cat_id) for cat_id in video['category_id']]
    cover_img = video['cover_img'] or video['uri']

    video['full_cover_img'] = full_domain(cover_img + '.jpg', with_token=False)
    uri = video['uri'] + '_preview' if not can_play_all else video['uri']
    video['full_uri'] = full_domain(uri + '.mp4', user_id=user_id)
    video['can_play_all'] = can_play_all
    video['liked'] = videoservice.has_liked(user_id, video['id']) if user_id else False

    del video['uri']
    del video['cover_img']
    del video['disable']

    return video
