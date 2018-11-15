from django.conf.urls import url
from . import videoview

urlpatterns = [
    url(r'^$', videoview.Video.as_view()),
    url(r'^(?P<video_id>[1-9][0-9]*)$', videoview.VideoDetail.as_view()),
    url(r'^categories$', videoview.get_video_categories),

    url(r'^get_upload_token$', videoview.get_upload_token),
]
