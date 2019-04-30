from django.urls import include
from django.urls import path

from rest_framework import routers

from supply import views

router = routers.DefaultRouter()
router.register("order", views.OrderViewSet, base_name="transactions")
router.register("supplier", views.SupplierViewSet, base_name="suppliers")

urlpatterns = [
    path('', include(router.urls))
]
