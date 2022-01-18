from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display =['name', 'email']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display =['name', 'price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display =['customer', 'transaction_id']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display =['product', 'quantity']

@admin.register(ShippingAddress)
class ShippingAdmin(admin.ModelAdmin):
    list_display =['customer', 'order']









