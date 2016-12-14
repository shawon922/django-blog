from django.conf.urls import url
from . import views

app_name = 'posts'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create/$', views.create, name='create'),
    url(r'^update/(?P<slug>[\w-]+)/$', views.update, name='update'),
    url(r'^delete/(?P<slug>[\w-]+)/$', views.delete, name='delete'),
    url(r'^detail/(?P<slug>[\w-]+)/$', views.detail, name='detail'),
]

