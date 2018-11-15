from django.conf.urls import url

from . import payview

urlpatterns = [
    url(r'ways$', payview.get_pay_ways),
    url(r'price$', payview.get_price),

]
