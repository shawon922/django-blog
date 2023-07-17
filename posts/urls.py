from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('update/<slug>', views.update, name='update'),
    path('delete/<slug>', views.delete, name='delete'),
    path('detail/<slug>', views.detail, name='detail'),
]

