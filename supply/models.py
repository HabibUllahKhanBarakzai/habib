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
    purchase_date = models.DateField(default=timezone.now())


class Order(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="order")
    order_at = models.DateField(null=True, blank=True)
    received_at = models.DateField(default=timezone.now())
    total_price = models.PositiveIntegerField()
    price_payed = models.PositiveIntegerField()
    installment_amount = models.PositiveIntegerField()
    next_installment_due = models.DateField(default=timezone.now() + timezone.timedelta(days=30))
    amount_remaining = models.PositiveIntegerField()
    installments_history = ArrayField(JSONField(), verbose_name="History of installments payed",
                                      default=list)
    actual_price = models.PositiveIntegerField(default=0, verbose_name="Price after discount")


class Discount(models.Model):
    PERCENTAGE = 0
    ABSOLUTE = 1
    DISCOUNT_CHOICE = (
        (PERCENTAGE, 'PERCENTAGE'),
        (ABSOLUTE, 'ABSOLUTE')
    )

    discount_type = models.PositiveIntegerField(choices=DISCOUNT_CHOICE, default=PERCENTAGE)
    amount = models.PositiveIntegerField(default=0)
    reason = models.CharField(max_length=100)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name="order_discounts")