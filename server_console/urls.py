"""aa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from .controller.users import urls as users_urls
from .controller.videos import urls as videos_urls
from .controller.pay import urls as pay_urls
from .controller.operators import urls as operators_urls
from .controller.orders import urls as orders_urls


urlpatterns = [
    url(r'^users/', include(users_urls)),
    url(r'^videos/', include(videos_urls)),
    url(r'^pay/', include(pay_urls)),
    url(r'^orders/', include(orders_urls)),
    url(r'^operators/', include(operators_urls)),
]
