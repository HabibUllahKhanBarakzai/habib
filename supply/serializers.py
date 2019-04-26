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
        my_order = Order()
        my_order.supplier = supplier
        my_order.order_at = self.initial_data.get("ordered_at", tod)
        my_order.received_at = self.initial_data.get("recieved_at", tod)
        my_order.price_payed = self.initial_data.get("price_payed", 0)
        my_order.discount = self.initial_data.get("discount", 0)
        my_order.installment_amount = self.initial_data.get("installment_amount")
        my_order.next_installment_due = self.initial_data.get("next_installment_due", tod)
        my_order.total_price = 0
        my_order.amount_remaining = 0
        my_order.installments_history = []
        my_order.save()

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
            purchase.order = my_order
            print(my_mobile.id)
            purchase.mobile = my_mobile
            purchase.save()

        my_order.total_price = price_complete
        my_order.next_installment_due = self.initial_data.get("next_installment_due", None)
        data = {
            "installment": my_order.price_payed,
            "date": today.strftime("%Y-%m-%d")
        }
        my_order.amount_remaining = my_order.actual_price - my_order.price_payed
        my_order.installments_history.append(data)
        my_order.save()
        return my_order

    def update(self, instance, validated_data):
        installment = self.initial_data.get("installment")
        if installment is None:
            raise ValueError("Please Enter installment amount")

        if installment > instance.amount_remaining:
            raise ValueError("remaining amount is less than instalment amount you are entering")

        today = datetime.datetime.now()

        instance.price_payed += installment
        instance.amount_remaining = instance.amount_remaining - installment
        data = {
            "installment": installment,
            "date": today.strftime("%Y-%m-%d")
        }
        instance.installments_history.append(data)
        instance.save()
        return instance
