from rest_framework.viewsets import ModelViewSet
from supply.models import Supplier, Order
from supply.serializers import OrderCreateSerializer, SupplierSerializer, OrderSerializer


class OrderViewSet(ModelViewSet):
    model = Order
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return OrderSerializer

        return OrderCreateSerializer


class SupplierViewSet(ModelViewSet):
    model = Supplier
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
