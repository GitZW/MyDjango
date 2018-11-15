from django.conf.urls import url

from . import orderview

urlpatterns = [
    # 订单
    url(r'^$', orderview.OrderList.as_view()),
]
