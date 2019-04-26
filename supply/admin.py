from django.contrib import admin
from.models import Supplier, Order, Purchase

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("company",)


@admin.register(Order)
class Order(admin.ModelAdmin):
    list_display = ('order_at', 'supplier', 'total_price')


@admin.register(Purchase)
class Order(admin.ModelAdmin):
    list_display = ('mobile', 'order', 'price', 'discount', 'purchase_date')