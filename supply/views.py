from rest_framework.viewsets import ModelViewSet
from supply.models import Supplier, Order
from supply.serializers import OrderCreateSerializer


class OrderViewSet(ModelViewSet):
    model = Order
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
