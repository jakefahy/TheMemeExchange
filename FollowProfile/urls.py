from django.urls import path

from . import views

urlpatterns = [
	path('<userID>/', views.index, name='index'),
	path('userToBeFollowed/<userID>', views.userfollow, name='userfollow'),
	path('userToBeUnfollowed/<userID>', views.userunfollow, name='userunfollow'),

]