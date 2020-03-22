from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='ProfilePage'),
    path('upload/', views.uploadMemeImg, name="uploadMemes")
]
