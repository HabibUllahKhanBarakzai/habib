from django.contrib import admin
from .models import User, Mobile, Transactions, Customer

#
# @admin.register(User)
# class CustomerAdmin(admin.ModelAdmin):
#     list_display = (name)

@admin.register(Mobile)
class MobileAdmin(admin.ModelAdmin):
    list_display = ('IMEA_number', )


@admin.register(User)
class MobileAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Transactions)
class MobileAdmin(admin.ModelAdmin):
    list_display = ('sold_item', )
    raw_id_fields = ('sold_item', 'customer')
