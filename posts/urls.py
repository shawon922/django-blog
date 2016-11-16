from django.conf.urls import url
from . import views

app_name = 'posts'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create/$', views.create, name='create'),
    url(r'^update/(?P<id>\d+)/$', views.update, name='update'),
    url(r'^delete/(?P<id>\d+)/$', views.delete, name='delete'),
    url(r'^detail/(?P<id>\d+)/$', views.detail, name='detail'),
]

