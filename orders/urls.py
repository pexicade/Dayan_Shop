from django.urls import path

from .views import view_cart, get_info

urlpatterns = [
    path('cart', view_cart, name='cart'),
    path('ajax/get_info', get_info, name='get_info'),
]