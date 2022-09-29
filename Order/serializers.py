from rest_framework import serializers
from .models import OrderProduct, BookOrder

class OrderProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = OrderProduct
		fields =  ['id', 'price', "product", "quantity"]

class OrderCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = BookOrder
		fields = '__all__'

class OrderItemCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = OrderProduct
		fields = "__all__"


class OrderViewSerializer(serializers.ModelSerializer):
	class Meta:
		model = BookOrder
		fields = ['id', 'user']

class AdminOrderViewSerializer(serializers.ModelSerializer):
	class Meta:
		model = BookOrder
		fields = '__all__'