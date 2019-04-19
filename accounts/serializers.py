from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.exceptions import ValidationError
import datetime
from accounts.models import Transactions, Customer, Our_User, Mobile


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
            customer = Customer.objects.get(user__CNIC_number=CNIC_number)

        except Customer.DoesNotExist:

            if Our_User.objects.filter(CNIC_number=CNIC_number).exists():
                user = Our_User.objects.get(CNIC_number=CNIC_number)
                customer_existing = Customer.objects.create(user=user)
                return customer_existing

            else:

                print(validated_data.get("date_of_birth"))
                print(type(validated_data))
                user = Our_User.objects.create(CNIC_number=CNIC_number,
                                               name=customer.get("name"),
                                               father_name=customer.get("father_name"),
                                               gender=customer.get("gender"),
                                               address=customer.get("address"),
                                               is_live_user=customer.get("is_live_user"),
                                               is_maintenance_user=customer.get(
                                                   "is_maintenance_user"))
                customer_new = Customer.objects.create(user=user)
                return customer_new

        else:
            return customer


class TransactionSerializer(Serializer):

    class Meta:
        model = Transactions
        fields = "__all__"

    def create(self, validated_data):

        CustomerSerializer = CustomerCreateSerializer()
        customer = CustomerSerializer.create(validated_data=self.context['request'].data)
        mobile = self.initial_data.get("mobile")
        try:
            our_mobile = Mobile.objects.get(IMEA_number=mobile.get("IMEA_number"), is_sold=False)

        except Mobile.DoesNotExist:
            raise ValidationError("mobile with that IMEA number is not in inventory")

        else:
            insurer1 = self.initial_data.get("insurer_one")
            insurer2 = self.initial_data.get("insurer_two")
            user_1, is_created = Our_User.objects.get_or_create(name=insurer1.get("name"),
                                                                CNIC_number=insurer1.get(
                                                                    "cnic_number"))
            user_2, is_created = Our_User.objects.get_or_create(name=insurer2.get("name"),
                                                                CNIC_number=insurer2.get(
                                                                    "cnic_number"))
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
            customer.installments_payed.append(installment_history)
            customer.save()
            our_mobile.is_sold = True
            our_mobile.save()
            transaction = Transactions.objects.create(customer=customer,
                                                      sold_item=our_mobile,
                                                      date_of_sale=today,
                                                      previous_installment_payed=today,
                                                      amount_remaining=amount_remaining,
                                                      next_installment_due=next_installment,
                                                      insurer_one=user_1,
                                                      insurer_two=user_2,
                                                      number_of_installments_payed=1)
            return transaction

    def update(self, instance, validated_data):

        installment = self.initial_data.get("installment", None)
        today = datetime.datetime.now().date()

        instance.amount_payed = instance.amount_payed + installment
        instance.amount_remaining = instance.sold_item.price - instance.amount_payed
        instance.previous_installment_payed = today
        instance.number_of_installments_payed += 1
        data = {
            "date": today.strftime("%Y-%m-%d"),
            "amount": installment
        }
        instance.customer.installments_payed.append(data)
        instance.customer.save()
        next_installment = self.initial_data.get("next_installment_due", None)
        instance.next_installment_due = next_installment if next_installment is not None else (
                    today + datetime.timedelta(days=30))
        instance.save()

        return instance




