from django.conf.urls import url

from . import userview, feedbacksview

urlpatterns = [
    # 用户
    url(r'^$', userview.UserList.as_view()),
    url(r'^(?P<user_id>[1-9][0-9]*)$', userview.UserDetail.as_view()),

    # 反馈
    url(r'feedbacks$', feedbacksview.FeedbackView.as_view()),
    url(r'feedbacks/(?P<user_id>[1-9][0-9]*)/history$', feedbacksview.FeedbackHistoryView.as_view()),
    url(r'feedbacks/(?P<user_id>[1-9][0-9]*)$', feedbacksview.reply_user),

]
