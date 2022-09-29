from rest_framework import serializers
from Order.models import BookOrder, OrderProduct
from Product.models import Product, Category
from .models import CustomUser as User


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'first_name', 'middle_name', 'last_name','email','balance','role','region', 'zone','city', 'woreda', 'kebelle','Phone']
class UserCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['username','email','password']
		extra_kwargs = {'password': {'write_only': True}}
	def create(self, validated_data):
		user = User(
			email=validated_data['email'],
			username=validated_data['username']
			)
		user.set_password(validated_data['password'])
		user.save()
		return user

class UserProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['first_name', 'middle_name','last_name','region', 'zone','city', 'woreda', 'kebelle','Phone', "balance"]

class UserChangePasswordSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id','password', 'username']
