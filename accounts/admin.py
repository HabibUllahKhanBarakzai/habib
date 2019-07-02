from django.contrib import admin
from .models import Our_User, Mobile, Transactions, Customer, TransactionReturn

#
# @admin.register(User)
# class CustomerAdmin(admin.ModelAdmin):
#     list_display = (name)

@admin.register(Mobile)
class MobileAdmin(admin.ModelAdmin):
    list_display = ('imei_number', )


@admin.register(Our_User)
class MobileAdmin(admin.ModelAdmin):
    list_display = ('name', 'CNIC_number')


@admin.register(Transactions)
class MobileAdmin(admin.ModelAdmin):
    list_display = ('sold_item', 'get_user_name' )
    raw_id_fields = ('sold_item', 'customer', 'insurer_one', 'insurer_two')

    def get_user_name(self, obj):
        return obj.customer.user.name

    get_user_name.short_description = "name"


@admin.register(TransactionReturn)
class MobileAdmin(admin.ModelAdmin):
    list_display = ('transaction', 'date_of_return')