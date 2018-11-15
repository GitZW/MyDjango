from django.conf.urls import url
from . import videoview

urlpatterns = [
    # 视频
    url(r'^$', videoview.get_videos),
    url(r'^(?P<video_id>[1-9][0-9]*)$', videoview.VideoDetail.as_view()),
    url(r'^(?P<video_id>[1-9][0-9]*)/like$', videoview.add_like),

    # 视频模块
    url(r'^categories$', videoview.get_video_categories),

]