from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField

from django.utils import timezone
from accounts.models import Mobile


class Supplier(models.Model):
    company = models.CharField(max_length=30)


class Purchase(models.Model):
    mobile = models.OneToOneField(Mobile, on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name="purchase")

    price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    purchase_date = models.DateField(default=timezone.now().date())


class Order(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="order")
    order_at = models.DateField(null=True, blank=True)
    received_at = models.DateField(default=timezone.now().date())
    total_price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    price_payed = models.PositiveIntegerField()
    installment_amount = models.PositiveIntegerField()
    next_installment_due = models.DateField(default=timezone.now().date() + timezone.timedelta(days=30))
    amount_remaining = models.PositiveIntegerField()
    installments_history = ArrayField(JSONField(), verbose_name="History of installments payed",
                                      default=list)

    @property
    def actual_price(self):
        return self.total_price - (self.total_price * (self.discount/100))