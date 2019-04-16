from django.db import models
from django.contrib.postgres.fields import ArrayField,JSONField


class User(models.Model):
    GENDER_OPTIONS = (
        ("Male", "Male"),
        ("FEMALE", "Female"),
        ("OTHER", "Other")
    )

    name = models.CharField( max_length=60, blank=False)
    father_name = models.CharField(max_length=60, blank=False)
    gender = models.CharField(choices=GENDER_OPTIONS, max_length=10, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=False)
    is_live_user = models.BooleanField(default=True, verbose_name='Is_Live_User')
    is_maintenance_user = models.BooleanField(default=False, verbose_name='Maintenance_User')
    address = models. CharField(max_length=250)
    CNIC_number = models.IntegerField(blank=False, unique=True)


class Mobile(models.Model):
    brand_choices = (
        ("Samsung", "Samsung"),
        ("IPhone", "IPhone"),
        ("QMobile", "QMobile"),
        ("Huawei", "Huawei"),
        ("Nokia", "Nokia")
    )
    status_choice = (
        ("used", "used"),
        ("New", "New")
    )

    brand = models.CharField(choices=brand_choices, max_length=20)
    price = models.PositiveIntegerField()
    type = models.CharField(max_length=10)
    mobile_status = models.CharField(choices=status_choice, max_length=5)
    IMEA_number = models.CharField(max_length=50, unique=True)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_customer")
    installments_payed = ArrayField(JSONField(), verbose_name="History of installments payed", default=[])


class Transactions(models.Model):
    sold_item = models.ForeignKey(Mobile, on_delete=models.CASCADE, related_name="sale")
    date_of_sale = models.DateField(default=None)
    amount_payed = models.PositiveIntegerField(default=0)
    insurer_one = models.ForeignKey(User, on_delete=models.CASCADE, related_name="first_insurer")
    insurer_two = models.ForeignKey(User, on_delete=models.CASCADE, related_name="second_insurer")
    next_installment_due = models.DateField(default=None, verbose_name="Next Installment Date")
    previous_installment_payed = models.DateField(default=None, verbose_name="Previous Installment Payed")
    number_of_installments_payed = models.PositiveIntegerField(default=0, verbose_name="Number Of Installments Payed")
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name="customer")
    is_return = models.BooleanField(default=False)