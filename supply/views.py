from rest_framework.viewsets import ModelViewSet
from supply.models import Supplier


class SupplyViewSet(ModelViewSet):
    model = Supplier
    queryset = Supplier.objects.all()

