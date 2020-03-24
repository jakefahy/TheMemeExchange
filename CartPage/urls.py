from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='cart'),
    path('removeItemFromCart/<int:img_id>/', views.removeItemFromCart, name='removeItemFromCart'),
    path('purchaseMeme/', views.purchaseMeme, name='purchaseMeme'),
]
