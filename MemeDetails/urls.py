from django.urls import path

from . import views

urlpatterns = [
    path('<int:image_id>/', views.index, name='details'),
    path('addToCart/<int:image_id>/', views.addToCart, name='addToCart'),
]