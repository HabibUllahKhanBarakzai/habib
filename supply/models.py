from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField

from accounts.models import Mobile
import datetime


class Supplier(models.Model):
    company = models.CharField(max_length=30)


class Purchase(models.Model):
    mobile = models.OneToOneField(Mobile, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    purchase_date = models.DateField(default=datetime.datetime.now().date())


class Order(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="order")
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="order")
    order_at = models.DateField(null=True, blank=True)
    received_at = models.DateField(default=datetime.datetime.now().date())
    total_price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    price_payed = models.PositiveIntegerField()
    installment_amount = models.PositiveIntegerField()
    next_installment_due = models.DateField(default=datetime.datetime.now().date() + datetime.timedelta(days=30))
    installments_history = ArrayField(JSONField(), verbose_name="History of installments payed",
                                      default=list)

