from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.exceptions import ValidationError
from accounts.models import Transactions, Customer, User, Mobile


class CustomerCreateSerializer(Serializer):
    class Meta:
        model = Customer
        fields = "__all__"

    def create(self, validated_data):
        customer = self.initial_data.get("customer", None)
        CNIC_number = customer.get("cnic_number", None)

        try:
            customer = Customer.objects.get(user__CNIC_number=CNIC_number)

        except Customer.DoesNotExist:

            if User.objects.filter(CNIC_number=CNIC_number).exists():
                user = User.objects.get(CNIC_number=CNIC_number)
                customer_existing = Customer.objects.create(user=user)
                return customer_existing

            else:

                print(validated_data.get("date_of_birth"))
                print(type(validated_data))
                user = User.objects.create(CNIC_number=CNIC_number,
                                           name=customer.get("name"),
                                           father_name=customer.get("father_name"),
                                           gender=customer.get("gender"),
                                           address=customer.get("address"),
                                           is_live_user=customer.get("is_live_user"),
                                           is_maintenance_user=customer.get("is_maintenance_user"))
                customer_new = Customer.objects.create(user=user)
                return customer_new

        else:
            return customer


class TransactionSerializer(CustomerCreateSerializer):
    def create(self, validated_data):

        customer = super().create(validated_data)
        print("in create")
        print(customer)
        mobile = validated_data.get("mobile")
        try:
            mobile = Mobile.objects.get(IMEA_number=mobile.get("IMEA_number"))

        except Mobile.DoesNotExist:
            raise ValidationError("IMEA number is incorrect")

        else:
            transaction = Transactions.objects.create(customer=customer,
                                                      sold_item=mobile)
            return transaction



