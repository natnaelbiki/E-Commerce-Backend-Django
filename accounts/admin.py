from django.contrib import admin
from .models import CustomUser


admin.site.register(CustomUser)



admin.site.site_header = "E-Commerce Admin"
admin.site.site_title = "E-Commerce Admin Portal"
admin.site.index_title = "Welcome to E-Commerce Administration Portal"
