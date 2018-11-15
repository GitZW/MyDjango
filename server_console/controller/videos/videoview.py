# -*- coding: utf-8 -*
import uuid
import logging
from django.views.decorators.http import require_GET, require_POST

from core_video.service import videoservice
from utils.common.decorators import validate_form, require_login
from .videoform import *
from utils.domainutils import *
from django.views.generic import View

from django.utils.decorators import method_decorator
from core_operator.service import operatorservice
from utils.common import fs
from datetime import datetime

logger = logging.getLogger(__name__)


class Video(View):
    @method_decorator(validate_form(VideoListForm))
    def get(self, request, cleaned_data):
        total, videos = videoservice.get_video_list(**cleaned_data)
        return dict(total=total, videos=[wrap_videos(video)for video in videos])

    @method_decorator(validate_form(AddVideoForm))
    def post(self, request, cleaned_data):
        uploader_id = request.user.id
        video_id = videoservice.add_video(**cleaned_data, uploader_id=uploader_id)
        return dict(id=video_id)


class VideoDetail(View):
    def get(self, request, video_id):
        video = videoservice.get_video_by_id(int(video_id))
        return wrap_videos(video)

    @method_decorator(validate_form(UpdateVideoForm))
    def put(self, request, video_id, cleaned_data):
        videoservice.update_video(int(video_id), **cleaned_data)
        return dict(id=1)

    def delete(self, request, video_id):
        return dict(id=videoservice.delete_video(int(video_id)))


@require_GET
def get_upload_token(request):
    return dict(token=fs.get_token(uuid.uuid4().hex, deadline=int(datetime.now().timestamp() + 30 * 60)))


@require_GET
def get_video_categories(reuqest):
    return videoservice.get_categories()


def wrap_videos(video):
    """
    :param user_id:
    :param videos:
    :return:
    """
    category_dict = videoservice.get_category_dict()
    video['category'] = [category_dict.get(cat_id) for cat_id in video['category_id']]
    cover_img = video['cover_img'] or video['uri']
    video['full_cover_img'] = full_domain(cover_img + '.jpg', with_token=False)
    video['full_uri'] = full_domain(video['uri'] + '.mp4')
    video['uploader'] = operatorservice.get_operator_id_and_name_dict(video['uploader_id'])

    del video['uri']
    del video['cover_img']

    return video
