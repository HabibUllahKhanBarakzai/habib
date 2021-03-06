from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.exceptions import ValidationError

import datetime

from accounts.models import Transactions, Customer, Our_User, Mobile, TransactionReturn
from django.http import Http404
from django.db.models import Q


class MobileSerializer(ModelSerializer):
    class Meta:
        model = Mobile
        fields = "__all__"


class UserSerializer(ModelSerializer):
    class Meta:
        model = Our_User
        fields = "__all__"


class CustomerSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = "__all__"


class GetTransactionSerializer(ModelSerializer):
    customer = CustomerSerializer()
    sold_item = MobileSerializer()
    insurer_one = UserSerializer()
    insurer_two = UserSerializer()

    class Meta:
        model = Transactions
        fields = "__all__"


class CustomerCreateSerializer(Serializer):
    class Meta:
        model = Customer
        fields = "__all__"

    def create(self, validated_data):

        customer = validated_data.get("customer", None)
        CNIC_number = customer.get("cnic_number", None)
        try:
            customers = Customer.objects.get(user__CNIC_number=CNIC_number)
        except Customer.DoesNotExist:

            if Our_User.objects.filter(CNIC_number=CNIC_number).exists():
                user = Our_User.objects.get(CNIC_number=CNIC_number)
                user.name = customer.get("name")
                user.save()
                customer_existing = Customer.objects.create(user=user)
                return customer_existing

            else:

                user = Our_User.objects.create(CNIC_number=CNIC_number,
                                               name=customer.get("name"),
                                               father_name=customer.get("father_name"),
                                               gender=customer.get("gender"),
                                               house_address=customer.get("house_address"),
                                               business_address=customer.get("business_address"),
                                               phone_number=customer.get("phone_number")
                                               )

                customer_new = Customer.objects.create(user=user)
                return customer_new

        else:
            if customer.get("name", None):
                customers.user.name = customer.get("name", None)
                customers.user.save()
            return customers


class TransactionSerializer(Serializer):

    class Meta:
        model = Transactions
        fields = "__all__"

    def create(self, validated_data):

        if self.context['request'].data is None:
            raise Http404
        for val in validated_data:
            print(val)
        customer_serializer = CustomerCreateSerializer()
        customer = customer_serializer.create(validated_data=self.context['request'].data)
        mobile = self.initial_data.get("mobile")
        try:
            our_mobile = Mobile.objects.get(imei_number=mobile.get("IMEI_number"), is_sold=False)

        except Mobile.DoesNotExist:
            raise ValidationError("mobile with that imei number is not in inventory")

        else:
            print("")
            # todo: improve the insurer so that all our_user fields will be populated for insurer
            insurer1 = self.initial_data.get("insurer_one")
            insurer2 = self.initial_data.get("insurer_two")

            user_1, is_created = Our_User.objects.get_or_create(CNIC_number=insurer1.get("cnic_number"))
            user_2, is_created = Our_User.objects.get_or_create(CNIC_number=insurer2.get("cnic_number"))
            user_1.name = insurer1.get("name")
            user_1.house_address = insurer1.get("house_address")
            user_1.office_address = insurer1.get("office_address")
            user_1.save()
            user_2.name=insurer2.get("name")
            user_2.house_address = insurer2.get("house_address")
            user_2.office_address = insurer2.get("office_address")
            user_2.save()

            today = datetime.datetime.now().date()

            price = our_mobile.price
            payed = self.initial_data.get("amount_payed")
            amount_remaining = price - payed
            next_installment = self.initial_data.get("next_installment") if self.initial_data.get(
                "next_installment") \
                else today + datetime.timedelta(days=30)

            installment_history = {
                "date": today.strftime("%Y-%m-%d"),
                "amount": payed
            }
            installment_amount = self.initial_data.get("installment")
            our_mobile.is_sold = True
            our_mobile.save()
            transaction = Transactions.objects.create(customer=customer,
                                                      sold_item=our_mobile,
                                                      date_of_sale=today,
                                                      amount_remaining=amount_remaining,
                                                      amount_payed=payed,
                                                      next_installment_due=next_installment,
                                                      insurer_one=user_1,
                                                      insurer_two=user_2,
                                                      number_of_installments_payed=1,
                                                      installment_amount=installment_amount)
            transaction.installments_payed.append(installment_history)
            transaction.save()
            return transaction

    def update(self, instance, validated_data):

        if instance.is_complete:
            return ValidationError("Transaction is completed, Customer has payed its dues")

        installment = self.initial_data.get("installment", None) if self.initial_data.get("installment")\
            else instance.installment_amount

        today = datetime.datetime.now().date()
        if installment > instance.amount_remaining:
            raise ValidationError("amount remaining is less than installment amount you are entering")

        instance.amount_payed = instance.amount_payed + installment
        instance.amount_remaining = instance.sold_item.price - instance.amount_payed
        instance.number_of_installments_payed += 1
        data = {
            "date": today.strftime("%Y-%m-%d"),
            "amount": installment
        }
        instance.installments_payed.append(data)
        next_installment = self.initial_data.get("next_installment_due", None)
        instance.next_installment_due = next_installment if next_installment is not None else (
                    today + datetime.timedelta(days=30))

        if instance.amount_remaining == 0:
            instance.is_complete = True
        instance.save()
        return instance


class TransactionReturnSerializer(ModelSerializer):
    class Meta:
        model = TransactionReturn
        fields = "__all__"

    def create(self, validated_data):
        transaction_id = self.initial_data.get("transaction", None)
        mobile_sold = self.initial_data.get("imei_number", None)
        transactions = None
        if transaction_id:
            try:
                transactions = Transactions.objects.get(id=transaction_id)
            except Transactions.DoesNotExist:
                if mobile_sold:
                    pass
                else:
                    raise Http404

        if mobile_sold:
            try:
                transactions = Transactions.objects.get(sold_item__imei_number=mobile_sold)
            except Transactions.DoesNotExist:
                raise Http404

        transaction_return = TransactionReturn()
        transaction_return.transaction = transactions
        transaction_return.amount_returned = self.initial_data.get("amount_returned")
        transaction_return.date_of_return = self.initial_data.get("date", datetime.datetime.now().date())
        transaction_return.reason = self.initial_data.get("reason", None)
        Transactions.returned = True
        transaction_return.save()
        transactions.save()
        return transaction_return


class ListTransactionReturnSerializer(ModelSerializer):
    transaction = GetTransactionSerializer(many=False)

    class Meta:
        model = TransactionReturn
        fields = "__all__"