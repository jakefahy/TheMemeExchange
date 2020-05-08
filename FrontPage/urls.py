from django.urls import path

from . import views

urlpatterns = [
    path('',views.index, name = 'index'),
    path('search/',views.searchByTag,name="searchByTag"),
    path('unlock/', views.unlock, name='unlock')
    ]
