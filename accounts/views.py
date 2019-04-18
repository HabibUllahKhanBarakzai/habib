from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from accounts.models import Transactions
from accounts.serializers import TransactionSerializer, GetTransactionSerializer


class TransactionViewSet(ModelViewSet):

    queryset = Transactions.objects.all()
    model = Transactions

    def get_serializer_class(self):
        print("in views")
        if self.action in ['list', 'retrieve']:
            return GetTransactionSerializer

        else:
            return TransactionSerializer
