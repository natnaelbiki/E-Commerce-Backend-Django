from django.contrib import admin
from .models import CustomerAction, CustomerTransaction

admin.site.register(CustomerAction)
admin.site.register(CustomerTransaction)
# Register your models here.
