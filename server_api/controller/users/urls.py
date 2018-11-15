from django.conf.urls import url

from . import userview, feedbacksview

urlpatterns = [
    # 用户
    url(r'login$', userview.login),
    url(r'register$', userview.register),
    url(r'logout$', userview.logout),
    url(r'info$', userview.get_user_info),

    # 反馈
    url(r'feedbacks$', feedbacksview.FeedbackView.as_view()),

]
