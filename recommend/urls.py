from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^user/(?P<userid>[0-9]+)/$',
        views.get_user_info,
        name='get_user_info'),
    url(r'^attraction/(?P<attrid>[0-9]+)/$',
        views.get_attraction_info,
        name='get_attraction_info'),
]
