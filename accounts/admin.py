from django.contrib import admin
from .models import User, Mobile, Sale, Customer


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name","date_of_birth")


@admin.register(Mobile)
class Mobile(admin.ModelAdmin):
    list_display = ("brand", "price", "type", "mobile_status")


@admin.register(Sale)
class Mobile(admin.ModelAdmin):
    list_display = ("get_email", "get_first_name","date_of_sale", "payable_payment")
    raw_id_fields = ("sold_item", "customer")

    def get_email(self, obj):
        return obj.customer.user.first_name

    def get_first_name(self, obj):
        return obj.customer.user.first_name


@admin.register(Customer)
class Mobile(admin.ModelAdmin):
    list_display = ('user', 'date_to_return', "remaining_amount")