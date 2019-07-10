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
    list_display = ('get_name', 'get_mobile_imei', 'get_mobile_type', 'date_of_return', 'amount_returned', 'reason')
    raw_id_fields = ('transaction', )
    search_fields = ('transaction__customer__user__name', )

    def get_name(self, obj):
        return obj.transaction.customer.user.name

    get_name.short_description = "customer_name"

    def get_mobile_imei(self, obj):
        return obj.transaction.sold_item.imei_number

    get_mobile_imei.short_description = "imei_number"

    def get_mobile_type(self, obj):
        return obj.transaction.sold_item.type

    get_mobile_type.short_description = "mobile_type"


