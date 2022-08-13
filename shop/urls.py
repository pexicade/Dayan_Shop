from django.urls import path

from .views import index, itemView, get_item

urlpatterns = [
    path('',index.as_view(),name="index"),
    path('<str:item_type>/<int:item_id>',itemView,name="item"),
    path('ajax/get_item',get_item,name="get_item"),

]
