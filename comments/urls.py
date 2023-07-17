from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('detail/{id}', views.comment_thread, name='thread'),
    path('delete/{id}', views.delete_comment, name='delete'),
    path('edit/{id}', views.edit_comment, name='edit'),
]
