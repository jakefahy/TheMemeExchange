from django.urls import path

from . import views

urlpatterns = [
    path('',views.index, name = 'index'),
    path('search/',views.searchByTag,name="searchByTag"),
    path('followFeed/',views.sortByFollowing, name='sortByFollowing'),
    path('unlock/', views.unlock, name='unlock')
    ]
