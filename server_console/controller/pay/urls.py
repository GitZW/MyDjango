from django.conf.urls import url

from . import payview

urlpatterns = [
    url(r'ways$', payview.PaywaysView.as_view()),
    url(r'ways/(?P<way_id>[1-9][0-9]*)$', payview.PaywaysDetailView.as_view()),

    ]