from django.contrib import admin
from .models import Our_User, Mobile, Transactions, Customer, TransactionReturn

#
# @admin.register(User)
# class CustomerAdmin(admin.ModelAdmin):
#     list_display = (name)

@admin.register(Mobile)
class MobileAdmin(admin.ModelAdmin):
    list_display = ('imei_number', 'is_sold', 'type' ,'price')
    search_fields = ('imei_number', )
    list_filter = ('is_sold', )


@admin.register(Our_User)
class MobileAdmin(admin.ModelAdmin):
    list_display = ('name', 'CNIC_number', 'date_of_birth', 'house_address')


@admin.register(Transactions)
class MobileAdmin(admin.ModelAdmin):
    list_display = ('id', 'sold_item', 'get_user_name', 'returned', 'number_of_installments_payed',
                    'next_installment_due', 'installment_amount')
    raw_id_fields = ('sold_item', 'customer', 'insurer_one', 'insurer_two')
    list_filter = ('is_complete', 'returned')

    def get_user_name(self, obj):
        return obj.customer.user.name

    get_user_name.short_description = "name"


@admin.register(TransactionReturn)
class MobileAdmin(admin.ModelAdmin):
    list_display = ('transaction', 'date_of_return')