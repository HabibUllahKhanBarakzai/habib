from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField


class Our_User(models.Model):
    GENDER_OPTIONS = (
        ("Male", "Male"),
        ("FEMALE", "Female"),
        ("OTHER", "Other")
    )

    name = models.CharField(max_length=60, blank=False)
    father_name = models.CharField(max_length=60, blank=True)
    gender = models.CharField(choices=GENDER_OPTIONS, max_length=10, null=True, blank=True)
    phone_number = models.CharField(max_length=14, default="")
    date_of_birth = models.DateField(null=True, blank=True)
    is_live_user = models.BooleanField(default=True, verbose_name='Is Live User')
    house_address = models.CharField(max_length=250)
    business_address = models.CharField(max_length=250, default="")
    CNIC_number = models.CharField(blank=False, unique=True, max_length=15)


class Mobile(models.Model):
    status_choice = (
        ("used", "used"),
        ("New", "New")
    )

    price = models.PositiveIntegerField()
    type = models.CharField(max_length=10)
    imei_number = models.CharField(max_length=50, unique=True)
    is_sold = models.BooleanField(default=False, verbose_name="Is product sold")


class Customer(models.Model):
    user = models.OneToOneField(Our_User, on_delete=models.CASCADE, related_name="user_customer")


class Transactions(models.Model):
    sold_item = models.ForeignKey(Mobile, on_delete=models.CASCADE, related_name="sale")
    date_of_sale = models.DateField(default=None)
    amount_payed = models.PositiveIntegerField(default=0)
    amount_remaining = models.PositiveIntegerField(default=0)
    insurer_one = models.ForeignKey(
        Our_User, on_delete=models.CASCADE, related_name="first_insurer")
    insurer_two = models.ForeignKey(
        Our_User, on_delete=models.CASCADE, related_name="second_insurer")
    next_installment_due = models.DateField(default=None, verbose_name="Next Installment Date")
    number_of_installments_payed = models.PositiveIntegerField(
        default=0, verbose_name="Number Of Installments Payed")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customer", unique=False)
    returned = models.BooleanField(default=False)
    installments_payed = ArrayField(JSONField(), verbose_name="History of installments payed",
                                    default=list)
    installment_amount = models.PositiveIntegerField()


class TransactionReturn(models.Model):
    transaction = models.OneToOneField(Transactions, on_delete=models.CASCADE, related_name="return_transaction")
    date_of_return = models.DateField(default=None)
    amount_returned = models.PositiveIntegerField()
    reason = models.CharField(null=True, blank=True, max_length=450)
