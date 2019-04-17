from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from accounts.models import Transactions
from accounts.serializers import TransactionSerializer, GetTransactionSerializer


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {
            'user': request.user.first_name,
            'message': 'Hello, World!'}
        return Response(content)


class TransactionViewSet(ModelViewSet):

    queryset = Transactions.objects.all()
    model = Transactions

    def get_serializer_class(self):

        if self.action in ['list', 'retrieve']:
            return GetTransactionSerializer

        else:
            return TransactionSerializer
