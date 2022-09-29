from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import generics, permissions
from django.views.decorators.csrf import csrf_exempt
from .serializers import UserSerializer, UserProfileSerializer, UserChangePasswordSerializer
from .models import CustomUser as User
from api.permissions import ReadOnly
from rest_framework.parsers import JSONParser
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
import re
from django.contrib.auth import authenticate
from Order.models import OrderProduct, BookOrder
from Notification.models import CustomerAction, CustomerTransaction

class Login(APIView):
	permission_classes = [ReadOnly,]
	serializer_class = UserSerializer

	def post(self, request):
		username = request.data.get('username')
		password = request.data.get('password')
		try:
			user = authenticate(request, username=username, password=password)
			if not user:
				try:
					user = User.objects.all().filter(username=username)
					if not user:
						return JsonResponse({"status": 0,'message':'unable to login. user with this username is not found'})
					elif user:
						return JsonResponse({"status": 0,'message':'unable to login. incorrect password'})
				except Exception as e:
						return JsonResponse({"status": 0,'message':'unable to login. '+str(e)})	
			else:
				try:
					order = BookOrder.objects.get(user=user)
				except:
					order = BookOrder.objects.create(user=user)
				try:
					token = Token.objects.get(user=user)
				except:
					token = Token.objects.create(user=user)
			print('role '+user.role)
			return JsonResponse({'status': 1,'message': 'login successful','token':str(token),'id': user.id, 'oid': order.id, 'role': user.role })
		except Exception as e:
			return JsonResponse({"status": 0,'message':'login failed. '+str(e)})
		

@csrf_exempt
def login(request):
	if request.method == 'POST':
		try:
			data = JSONParser().parse(request)
			user = authenticate(request, username=data['username'],	password=data['password'])
			if not user:
				try:
					user = User.objects.all().filter(username=data['username'])
					if not user:
						return JsonResponse({"status": 0,'message':'unable to login. user with this username is not found'})
					else:
						return JsonResponse({"status": 2,'message':'unable to login. incorrect password'})
				except Exception as e:
					return JsonResponse({"status": 3,'message':'unable to login. '+str(e)})
			else:
				try:
					order = BookOrder.objects.get(user=user)
				except:
					order = BookOrder.objects.create(user=user)
				try:
					token = Token.objects.get(user=user)
				except:
					token = Token.objects.create(user=user)
				return JsonResponse({'status': 1,'message': 'login successful','token':str(token),'id':user.id, 'oid': order.id, 'role': user.role})
		except Exception as e:
			return JsonResponse({'status': 0, 'message': 'unable to login '+str(e)})
		
		
@csrf_exempt
def signup(request):
	if request.method == 'POST':
		try:
			data = JSONParser().parse(request) # data is a dictionary
			user = User.objects.create_user(
									username=data['username'], email=data['email'],
										password=data['password'], role='customer', balance=0)
			user.save()
			token = Token.objects.create(user=user)
			order = BookOrder.objects.create(user=user)
			return JsonResponse({'status': 1, 'message':'user has been created','token':str(token),'id': user.id, 'oid': order.id, 'role': user.role})
		except IntegrityError:
			return JsonResponse({'status': 2,'message':' already taken. choose another username'})

class AdminUserDetail(APIView):
	permission_classes= (permissions.IsAuthenticated,)
	serializer_class = UserSerializer
	
	def get(self, request):
		user = User.objects.all()
		u_it = {}
		for x in user:
			u_i = {'id': x.id, 'username': str(x)}
			u_it.setdefault(x.id, u_i)
		#print(u_it)
		return JsonResponse({'status': 0, 'message': 'all good', 'users': u_it})

class AdminNewUser(generics.CreateAPIView):
	permission_classes= (permissions.IsAuthenticated,)
	serializer_class = UserSerializer

	def post(self, request):
		try:
			username = request.data.get('username')
			password = request.data.get('password')
			role = request.data.get("role") 
			balance = 0
			user = User.objects.create(username=username, password=password, role=role, balance=balance)
			return JsonResponse({'status': 1, 'message': 'User has been created successfully'})
		except Exception as e:
			return JsonResponse({'status': 0, 'message': str(e)})

class AdminUpdateUser(generics.RetrieveUpdateDestroyAPIView):
	permission_classes= (permissions.IsAuthenticated,)
	serializer_class = UserSerializer
	queryset = User.objects.all()

	def delete(self, request, pk):
		try:
			user = User.objects.get(pk=pk)
			if not user:
				return JsonResponse({'status': 0, 'message': 'user couldnt be found'})
			user.delete()
			return JsonResponse({'status': 1, 'message': 'user has been deleted successfully'})
		except Exception as e:
			return JsonResponse({'status': 0, 'message': str(e)})
	def put(self, request, pk):
		try:
			user = User.objects.get(pk=pk)
			if not user:
				return JsonResponse({'status': 0, 'message': 'user couldnt be found'})
			role = request.data.get("role") 
			balance = request.data.get("balance")
			user.role = role
			if not balance:
				balance = 0
			user.balance = balance
			user.save()
			return JsonResponse({'status': 1, 'message': 'user ' +user.username+' has been updated successfully'})
		except Exception as e:
			return JsonResponse({'status': 0, 'message': str(e)})

class UserDetail(APIView):
	permission_classes= (permissions.IsAuthenticated,)
	serializer_class = UserSerializer

	def get_object(self, pk):
		try:
			return User.objects.get(pk=pk)
		except:
			return None
	def get(self, request, pk, format=None):
		user = self.get_object(pk)
		if not user:
			return JsonResponse({'status': 0, 'message': 'User with this id not found'})
		serializer = UserSerializer(user)
		return JsonResponse(serializer.data, safe=False)


class UserEditDetail(APIView):
	permission_classes = [permissions.IsAuthenticated,]
	serializer_class = UserProfileSerializer


	def get_object(self, pk):
		try:
			return User.objects.get(pk=pk)
		except:
			return None

	def get(self, request, pk, format=None):
		user = self.get_object(pk)
		if not user:
			return JsonResponse({'status': 0, 'message': 'User with this id not found'})
		serializer = UserProfileSerializer(user)
		return JsonResponse(serializer.data)


	def post(self, request, pk, format=None):
		try:
			user = self.get_object(pk)
		except:
			return JsonResponse({'status': 0, 'message': 'User with this id not found'})
		
		first_name = request.data.get("first_name", None)
		middle_name = request.data.get("middle_name", None)
		last_name = request.data.get("last_name", None)
		region = request.data.get("region", None)
		zone = request.data.get("zone", None)
		city = request.data.get("city", None)
		woreda = request.data.get("woreda", None)
		kebelle = request.data.get("kebelle", None) 
		phone = request.data.get("Phone", None)

		user.first_name = first_name
		user.middle_name = middle_name
		user.last_name = last_name
		user.region = region
		user.zone = zone
		user.city = city
		user.woreda = woreda
		user.kebelle = kebelle
		user.Phone = phone

		try:
			user.save()
			NewNotification(user=user, action="Profile Updated", message='Your profile updated successfully!')
			serializer = UserProfileSerializer(user)
			return JsonResponse({"status": 1,'message': 'Your profile updated successfully!',"user":serializer.data})
		except:
			return JsonResponse({'status': 0, 'message': 'There was something wrong while updating your profile.'})

class UserProfile(GenericAPIView):
	permission_classes = [permissions.IsAuthenticated,]
	serializer_class = UserProfileSerializer
	queryset = User.objects

	def get_user(id):
		return User.objects.filter(id=id)

	def post(self, request, *args, **kwargs):
		return self.get_user(request.data.id)

class UserChangePassword(APIView):
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = UserChangePasswordSerializer

	def get_user(self, pk):
		try:
			return User.objects.get(pk=pk)
		except:
			return None
	def post(self, request):
		uid = request.data.get("uid")
		user = self.get_user(uid)
		if not user:
			return JsonResponse({'status': 0, 'message': 'User with this id not found'})
		password = request.data.get('password')
		old_password = request.data.get('old_password')
		op = user.password
		#check old password & encrypt the new one
		try:
			user.set_password(password)
			user.save()
			NewNotification(user=user, action="Password Changed", message='Password Changed successfully')
			return JsonResponse({'status': 1, 'message': 'Password Changed successfully'})
		except:
			return JsonResponse({'status': 0, 'message': 'something went wrong please try again later'})

def NewNotification(user, action, message):
	try:
		notif = CustomerAction.objects.create(user=user, action=action, message=message)
		notif.save()
		return True
	except Exception as e:
		print(str(e))
		return False
# Create your views here.
