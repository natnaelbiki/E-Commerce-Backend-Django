from django.contrib import admin
from .models import OrderProduct, BookOrder


class OrderItemInline(admin.TabularInline):
	model = OrderProduct
	raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
	list_display = ['user']
	inlines = [OrderItemInline]


admin.site.register(BookOrder, OrderAdmin)# Register your models here.
