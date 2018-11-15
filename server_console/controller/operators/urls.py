from django.conf.urls import url

from . import operatorsview

urlpatterns = [
    # 用户
    url(r'^$', operatorsview.get_operator_list),
    url(r'^login$', operatorsview.login, name="cuser_login"),
    # url(r'^register$', operatorsview.register, name="cuser_register"),

]
