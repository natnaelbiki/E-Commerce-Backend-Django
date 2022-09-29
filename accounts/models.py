from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE = {("customer", "Customer"),("admin", "Admin"),("supplier", "Supplier"),("delivery", "Delivery")}



class CustomUser(AbstractUser):
	middle_name = models.CharField(max_length=20, null=True)
	role = models.CharField(max_length=20, null=False, choices=ROLE, default="customer")
	balance = models.PositiveIntegerField(null=False, blank=False, default=0)
	Phone = models.PositiveIntegerField(null=True)
	region = models.CharField(max_length=20, null=True)
	zone = models.CharField(max_length=20, null=True)
	city = models.CharField(max_length=20, null=True)
	woreda = models.CharField(max_length=20, null=True)
	kebelle = models.CharField(max_length=20, null=True)

	