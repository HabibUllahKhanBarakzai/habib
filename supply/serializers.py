from supply.models import Supplier, Order, Purchase, Discount
from accounts.models import Mobile

import datetime

from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError


class OrderCreateSerializer(Serializer):
    class Meta:
        model = Order
        fields = "__all__"

    def create(self, validated_data):
        supplier_id = self.initial_data.get("supplier_id")

        try:
            supplier = Supplier.objects.get(id=supplier_id)

        except Supplier.DoesNotExist:
            raise ValidationError("This supplier does not exists")

        today = datetime.datetime.now()
        tod = today.strftime("%Y-%m-%d")
        my_order = Order()
        my_order.supplier = supplier
        my_order.order_at = self.initial_data.get("ordered_at", None)
        my_order.received_at = self.initial_data.get("received_at", tod)
        my_order.price_payed = self.initial_data.get("price_payed", 0)
        my_order.installment_amount = self.initial_data.get("installment_amount")
        my_order.next_installment_due = self.initial_data.get("next_installment_due", today + datetime.timedelta(days=30))
        my_order.total_price = 0
        my_order.amount_remaining = 0
        my_order.installments_history = []
        my_order.save()

        purchases = self.initial_data.get("purchase")
        price_complete = 0
        for cell_phone in purchases:
            try:
                my_mobile = Mobile()
                purchase = Purchase()
                my_mobile.imei_number = cell_phone.get("IMEI_number")

            except IntegrityError:
                raise ValidationError("Mobile with that IMEI number already exists ")

            else:
                purchase.discount = cell_phone.get("discount", 0)
                purchase.purchase_date = cell_phone.get("purchase_date", datetime.datetime.now())
                purchase.price = cell_phone.get("price")
                my_mobile.price = purchase.price - purchase.discount
                price_complete += my_mobile.price
                my_mobile.type = cell_phone.get("mobile_type")
                my_mobile.save()
                purchase.order = my_order
                purchase.mobile = my_mobile
                purchase.save()


        my_order.total_price = price_complete
        my_order.actual_price = price_complete

        discounts = self.initial_data.get("discount")

        for discount in discounts:
            disc = Discount()
            disc.discount_type = discount.get("type", 0)
            disc.amount = discount.get("amount")
            disc.reason = discount.get("reason")
            disc.order = my_order
            if discount.get("type", 0) == 0:
                my_order.actual_price = my_order.actual_price - (my_order.actual_price * disc.amount/100)

            elif discount.get("type", 0) == 1:
                my_order.actual_price = my_order.actual_price - disc.amount
            disc.save()

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
        date = self.initial_data.get("date")
        if installment is None:
            raise ValidationError("Please Enter installment amount")

        if installment > instance.amount_remaining:
            raise ValidationError("remaining amount is less than instalment amount you are entering")

        today = datetime.datetime.now()

        instance.price_payed += installment
        instance.amount_remaining = instance.amount_remaining - installment
        data = {
            "installment": installment,
            "date": today.strftime("%Y-%m-%d") if not date else date
        }
        instance.installments_history.append(data)
        instance.save()
        return instance


class SupplierSerializer(ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"


class PurchaseSerializer(ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'


class DiscountSerializer(ModelSerializer):
    class Meta:
        model = Discount
        fields = "__all__"


class OrderSerializer(ModelSerializer):

    supplier = SupplierSerializer()
    purchase = PurchaseSerializer(many=True)
    discounts = DiscountSerializer(many=True, source='order_discounts')

    class Meta:
        model = Order
        fields = "__all__"
