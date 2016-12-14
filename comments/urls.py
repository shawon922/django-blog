from django.conf.urls import url
from . import views

app_name = 'comments'

urlpatterns = [
    url(r'^detail/(?P<id>\d+)/$', views.comment_thread, name='thread'),
    url(r'^delete/(?P<id>\d+)/$', views.delete_comment, name='delete'),
]

