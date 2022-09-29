from rest_framework import serializers
from .models import CustomerAction, CustomerTransaction
from django.utils import timezone

class ActionSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomerAction
		fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomerTransaction
		fields = '__all__'