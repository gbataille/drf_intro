"""drf_prez URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

from rest_framework.routers import DefaultRouter

from demo.views import naive
from demo.views.item_viewset import ItemViewset
from demo.views.rest_view import ListUsers
from demo.views.generic_view import BoardListView, UserListGenericView, UserRetrieveGenericView


router = DefaultRouter()
router.register(r'items', ItemViewset, base_name='item')

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^naive_view/$', naive.naive_view),
    url(r'^rest/list_users/$', ListUsers.as_view()),
    url(r'^generic/users/$', UserListGenericView.as_view()),
    url(r'^generic/users/(?P<email>.+)/$', UserRetrieveGenericView.as_view()),
    url(r'^generic/boards/$', BoardListView.as_view()),
]
