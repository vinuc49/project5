from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Item, Cart, Order, OrderItem

@admin.register(Item)
class ItemAdmin(SummernoteModelAdmin):
    list_display = ("name", "price", "description")
    search_fields = ['name', 'description']
    summernote_fields = ("description",)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("item", "user", "quantity")
    search_fields = ['item', 'user']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "total_price", "name", "phone", "email", "payment_id")
    search_fields = ['user', 'name', 'address', 'city', 'county', 'postcode', 'phone', 'email', 'payment_id']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "item", "quantity", "price")
    search_fields = ['order', 'item', 'quantity', 'price']