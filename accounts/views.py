import datetime

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework import status

from django.db.models import Q

from accounts.models import Transactions, Customer, Mobile, Our_User, TransactionReturn
# from accounts.filtersets import MobileFilter
from accounts.serializers import TransactionSerializer,\
    GetTransactionSerializer, CustomerSerializer, MobileSerializer, UserSerializer, TransactionReturnSerializer


class TransactionViewSet(ModelViewSet):

    queryset = Transactions.objects.all().select_related("customer", "sold_item", "insurer_one", "insurer_two")
    model = Transactions

    def get_serializer_class(self):

        if self.action in ['list', 'retrieve']:
            return GetTransactionSerializer

        else:
            return TransactionSerializer



class TransactionReportsViewSet(ReadOnlyModelViewSet):
    model = Transactions
    serializer_class = GetTransactionSerializer
    queryset = Transactions.objects.filter(is_complete=False, returned=False)

    def list(self, request, *args, **kwargs):

        type = request.query_params.get('type')
        start_date = datetime.datetime.now().strftime("%Y-%m-%d")
        end_date = request.query_params.get('end_date')

        print("start ",start_date)
        print("type parameter", type)

        if type is "0":
            print("in zero")
            high = self.queryset.filter(next_installment_due__gte=start_date, next_installment_due__lte=end_date)

        else:
            print("in else of type")
            high = self.queryset.filter(next_installment_due__lte=start_date)

        ser_high = self.get_serializer(data=high, many=True)

        ser_high.is_valid()
        print(ser_high.data)
        return Response(data=ser_high.data, status=status.HTTP_200_OK)


class CustomerViewSet(ModelViewSet):
    model = Customer
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()


class MobileViewSet(ModelViewSet):
    http_method_names = ('get', 'patch', 'put')
    model = Mobile
    serializer_class = MobileSerializer
    # filter_class = MobileFilter

    def get_queryset(self):
        imea_number = self.request.query_params.get("imei_number")
        sold = self.request.query_params.get("sold")
        queryset = Mobile.objects.filter(is_sold=False)
        if imea_number:
            queryset = queryset.filter(imei_number=imea_number)

        return queryset


class InsurerView(APIView):

    def get(self, request, *args, **kwargs):

        queryset = Our_User.objects.filter(Q(first_insurer__isnull=False) | Q(second_insurer__isnull=False))
        serialize = UserSerializer(data=queryset, many=True)
        serialize.is_valid()

        return Response(data=serialize.data, status=status.HTTP_200_OK)


class ReturnTransactionViewSet(ModelViewSet):

    model = TransactionReturn
    queryset = TransactionReturn.objects.all()
    serializer_class = TransactionReturnSerializer


class InventoryViewSet(ModelViewSet):
    model = Mobile
    queryset = Mobile.objects.all()
    serializer_class = MobileSerializer