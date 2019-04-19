import datetime

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ReadOnlyModelViewSet

from accounts.models import Transactions
from accounts.serializers import TransactionSerializer, GetTransactionSerializer


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
    serializer_class = TransactionSerializer
    queryset = Transactions.objects.all()

    def list(self, request, *args, **kwargs):
        _high = datetime.datetime.today() + datetime.timedelta(2)
        _medium = datetime.datetime.today() + datetime.timedelta(5)

        high = self.queryset.filter(next_installment_due__lte=_high)
        medium = self.queryset.filter(next_installment_due__lte=_medium,
                                      next_installment_due__gte=_high)
        low = self.queryset.filter(next_installment_due__gte=_medium)

        ser_high = self.get_serializer(data=high, many=True)
        ser_high.is_valid()
        ser_medium = self.get_serializer(data=medium, many=True)
        ser_medium.is_valid()
        ser_low = self.get_serializer(data=low, many=True)
        ser_low.is_valid()

        response_data = {
            'high': ser_high.data,
            'medium': ser_medium.data,
            'low': ser_low.data
        }
        print(response_data)

        return Response(response_data)
