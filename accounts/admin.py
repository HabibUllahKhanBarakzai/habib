from django.contrib import admin
from .models import OurUser, Mobile, Transactions, Customer

#
# @admin.register(User)
# class CustomerAdmin(admin.ModelAdmin):
#     list_display = (name)

@admin.register(Mobile)
class MobileAdmin(admin.ModelAdmin):
    list_display = ('IMEA_number', )


@admin.register(OurUser)
class MobileAdmin(admin.ModelAdmin):
    list_display = ('name', 'CNIC_number')


@admin.register(Transactions)
class MobileAdmin(admin.ModelAdmin):
    list_display = ('sold_item', )
    raw_id_fields = ('sold_item', 'customer')
