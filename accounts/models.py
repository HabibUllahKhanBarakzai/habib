from django.db import models


class User(models.Model):
    GENDER_OPTIONS = (
        ("Male", "Male"),
        ("FEMALE", "Female"),
        ("OTHER", "Other")
    )

    first_name = models.CharField( max_length=30, blank=True)
    last_name = models.CharField( max_length=30, blank=True)
    gender = models.CharField(choices=GENDER_OPTIONS,max_length=10, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_live_user = models.BooleanField(default=True, verbose_name='Is_Live_User')
    is_maintenance_user = models.BooleanField(default=False, verbose_name='Maintenance_User')
    address = models. CharField(max_length=250)


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


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_customer")
    date_to_return = models.DateField(default=None)

    @property
    def remaining_amount(self):
        return self.transaction.sold_item.price - self.transaction.payed_amount


class Sale(models.Model):
    sold_item = models.ForeignKey(Mobile, on_delete=models.CASCADE, related_name="sale")
    date_of_sale = models.DateField()
    payed_amount = models.PositiveIntegerField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="transaction")

    @property
    def payable_payment(self):
        return self.sold_item.price

    @property
    def amount_owed(self):
        return self.sold_item.price - self.payed_amount
