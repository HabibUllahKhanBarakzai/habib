from django.contrib import admin
from.models import Supplier, Order, Purchase, Discount

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("company",)


@admin.register(Order)
class Order(admin.ModelAdmin):
    list_display = ('id', 'order_at', 'supplier', 'total_price')


@admin.register(Purchase)
class Order(admin.ModelAdmin):
    list_display = ('mobile', 'order', 'price', 'discount', 'purchase_date')


@admin.register(Discount)
class Order(admin.ModelAdmin):
    list_display = ('id', 'order', 'amount')