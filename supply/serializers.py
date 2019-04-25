from .models import Supplier, Order, Purchase
from accounts.models import Mobile
import datetime
from rest_framework.serializers import Serializer


class OrderCreateSerializer(Serializer):
    class Meta:
        model = Order
        fields = "__all__"

    def create(self, validated_data):
        supplier_id = self.initial_data.get("supplier_id")
        supplier = Supplier.objects.get(id=supplier_id)
        today = datetime.datetime.now()
        tod = today.strftime("%Y-%m-%d")
        order = Order()
        order.supplier = supplier
        order.order_at = self.initial_data.get("ordered_at", tod)
        order.received_at = self.initial_data.get("recieved_at", tod)
        order.price_payed = self.initial_data.get("price_payed", 0)
        order.discount = self.initial_data.get("discount", 0)
        order.installment_amount = self.initial_data.get("installment_amount")
        order.next_installment_due = self.initial_data.get("next_installment_due", tod)

        purchases = self.initial_data.get("purchase")
        price_complete = 0
        for cell_phone in purchases:
            my_mobile = Mobile()
            purchase = Purchase()
            my_mobile.IMEA_number = cell_phone.get("IMEI_number")
            purchase.discount = cell_phone.get("discount", 0)
            purchase.purchase_date = cell_phone.get("purchase_date", datetime.datetime.now())
            purchase.price = cell_phone.get("price")
            my_mobile.price = purchase.price - purchase.discount
            price_complete += my_mobile.price
            my_mobile.type = cell_phone.get("mobile_type")
            my_mobile.save()
            print(my_mobile.id)
            purchase.mobile = my_mobile
            purchase.save()
            order.purchase = purchase

        order.total_price = price_complete
        order.next_installment_due = self.initial_data.get("next_installment_due", None)
        data = {
            "price_payed": order.price_payed,
            "date": today.strftime("%Y-%m-%d")
        }
        order.amount_remaining = order.actual_price - order.price_payed
        order.installments_history.append(data)
        order.save()
        return order
