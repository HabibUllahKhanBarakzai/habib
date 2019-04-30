from rest_framework.viewsets import ModelViewSet
from supply.models import Supplier, Order
from supply.serializers import OrderCreateSerializer, SupplierSerializer


class OrderViewSet(ModelViewSet):
    model = Order
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer


class SupplierViewSet(ModelViewSet):
    model = Supplier
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
