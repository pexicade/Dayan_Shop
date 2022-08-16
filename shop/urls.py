from django.urls import path

from .views import (
    index, itemView, get_item,
    add_to_cart, remove_from_cart, decrease_item_count_from_cart, clear_cart, get_cart,
    
    )

app_name = 'shop'
urlpatterns = [
    path('',index.as_view(),name="index"),
    path('<str:item_type>/<int:item_id>',itemView,name="item"),
    path('ajax/get_item',get_item,name="get_item"),
    path('ajax/add_to_cart',add_to_cart,name="add_to_cart"),
    path('ajax/remove_from_cart',remove_from_cart,name="remove_from_cart"),
    path('ajax/decrease_item_count_from_cart',decrease_item_count_from_cart,name="decrease_item_count_from_cart"),
    path('ajax/clear_cart',clear_cart,name="clear_cart"),
    path('ajax/get_cart',get_cart,name="get_cart"),
]
