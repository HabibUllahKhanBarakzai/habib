from django.urls import include
from django.urls import path

from rest_framework import routers

from accounts import views

router = routers.DefaultRouter()
router.register("transactions", views.TransactionViewSet, base_name="transactions")
router.register("reports", views.TransactionReportsViewSet, base_name="reports")

urlpatterns = [
    path('', include(router.urls))
]
