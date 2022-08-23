from django.contrib import admin

from .models import OrderItem, Order, Discount

admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Discount)