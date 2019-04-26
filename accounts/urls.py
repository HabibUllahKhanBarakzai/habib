from django.urls import include
from django.urls import path

from rest_framework import routers

from accounts import views

router = routers.DefaultRouter()
router.register("transactions", views.TransactionViewSet, base_name="transactions")
router.register("reports", views.TransactionReportsViewSet, base_name="reports")
router.register('mobile', views.MobileViewSet, base_name="mobile")
router.register('customer', views.CustomerViewSet, base_name="customer")

urlpatterns = [
    path('', include(router.urls))
]
