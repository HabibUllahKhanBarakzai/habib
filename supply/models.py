from django.db import models
from accounts.models import Our_User


class Supplier(models.Model):
    company = models.CharField(max_length=30)
    user = models.ForeignKey(Our_User, on_delete=models.CASCADE, related_name="supplier")
