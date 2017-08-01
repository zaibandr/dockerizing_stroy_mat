from django.contrib import admin
from .models import Order, Product, CartItem, Cart

# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'volume', 'status', 'address', 'name', 'tonar', 'time_of_receipt', 'phone_number', 'time_created')
    list_filter = ('status', 'time_created',)
    search_fields = ('address',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name',)
    # list_filter = ('manager')
    search_fields = ('name',)


class CartAdmin(admin.ModelAdmin):
    pass


class CartItemAdmin(admin.ModelAdmin):
    pass


admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
