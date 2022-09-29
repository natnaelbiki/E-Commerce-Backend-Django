from rest_framework import generics, permissions
from django.utils import timezone
from rest_framework.views import APIView
from .serializers import ProductSerializer, CategorySerializer
from Product.models import Product, Category
import math
from Notification.models import CustomerAction, CustomerTransaction
from Notification.serializers import ActionSerializer, TransactionSerializer
from accounts.models import CustomUser as User
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model # new
from rest_framework import filters


#index view
class Home(generics.ListAPIView):
	permission_classes= (permissions.IsAuthenticatedOrReadOnly,)
	serializer_class = ProductSerializer
	queryset = Product.objects.all().filter(available=True).order_by('name')

class AdminViewProducts(generics.ListAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	serializer_class = ProductSerializer
	queryset = Product.objects.all()

class AdminAddNewProducts(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	serializer_class = ProductSerializer
	def post(self, request):
		try:
			user = request.user
			name = request.data.get('name')
			price = float(request.data.get('price'))
			category = request.data.get('categories')
			category = Category.objects.get(pk=category)
			if not category:
				return JsonResponse({'status': 0, 'message': 'There is a problem please try again'})
			description = request.data.get('description')
			stock = int(request.data.get('stock'))
			if stock == 0:
				available = False
			else:
				available = True
			unit = request.data.get('unit')
			if not user:
				return JsonResponse({'status': 0, 'message': 'There is a problem please try again'})
			try:
				product = Product.objects.create(name=name, price=price, stock=stock, available=available, category=category, description=description, added_by=user)
				product.save()
				return JsonResponse({'status': 1, 'message': 'product '+name+ ' has been saved successfully'})
			except Exception as e:
				return JsonResponse({'status': 0, 'message': str(e)})
		except Exception as e:
			return JsonResponse({'status': 0, 'message': str(e)})

class AdminUpdateProduct(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	serializer_class = ProductSerializer
	queryset = Product.objects.all()
	def delete(self, request, pk):
		try:
			product = Product.objects.get(pk=pk)
			product.delete()
			return JsonResponse({'status': 1, 'message': 'product '+name+ ' has been deleted successfully'})
		except Exception as e:
			return JsonResponse({'status': 0, 'message': str(e)})

	def put(self, request, pk):
		try:
			product = Product.objects.get(pk=pk)
			if not product:
				return JsonResponse({'status': 0, 'message': 'There is a problem please try again'})
			name = request.data.get('name')
			user = request.user
			price = float(request.data.get('price'))
			category = request.data.get('categories')
			category = Category.objects.get(pk=category)
			if not category:
				return JsonResponse({'status': 0, 'message': 'There is a problem please try again'})
			description = request.data.get('description')
			stock = int(request.data.get('stock'))
			if stock == 0:
				available = False
			else:
				available = True
			unit = request.data.get('unit')
			if not user:
				return JsonResponse({'status': 0, 'message': 'There is a problem please try again'})
			try:
				product.name=name 
				product.price=price
				product.stock=stock
				product.available=available
				product.category=category
				product.description=description
				product.added_by=user
				product.save()
				return JsonResponse({'status': 1, 'message': 'product '+name+ ' has been updated successfully'})
			except Exception as e:
				return JsonResponse({'status': 0, 'message': str(e)})
		except Exception as e:
			return JsonResponse({'status': 0, 'message': str(e)})

class SupplierViewProducts(generics.ListAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	serializer_class = ProductSerializer
	def get_queryset(self):
		user = self.request.user
		return Product.objects.all().filter(added_by=user)

class SupplierAddNewProducts(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	serializer_class = ProductSerializer
	def post(self, request):
		try:
			user = request.user
			name = request.data.get('name')
			price = float(request.data.get('price'))
			category = request.data.get('categories')
			category = Category.objects.get(pk=category)
			if not category:
				return JsonResponse({'status': 0, 'message': 'There is a problem please try again'})
			description = request.data.get('description')
			stock = int(request.data.get('stock'))
			if stock == 0:
				available = False
			else:
				available = True
			unit = request.data.get('unit')
			if not user:
				return JsonResponse({'status': 0, 'message': 'There is a problem please try again'})
			try:
				product = Product.objects.create(name=name, price=price, stock=stock, available=available, category=category, description=description, added_by=user)
				product.save()
				return JsonResponse({'status': 1, 'message': 'product '+name+ ' has been saved successfully'})
			except Exception as e:
				return JsonResponse({'status': 0, 'message': str(e)})
		except Exception as e:
			return JsonResponse({'status': 0, 'message': str(e)})

class SupplierUpdateProduct(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	serializer_class = ProductSerializer
	queryset = Product.objects.all()
	def delete(self, request, pk):
		try:
			product = Product.objects.get(pk=pk)
			user = request.user
			if not (product.added_by == user):
				return JsonResponse({'status': 0, 'message': 'you dont have the previllage to delete this product'})
			product.delete()
			return JsonResponse({'status': 1, 'message': 'product '+name+' has been deleted successfully'})
		except Exception as e:
			return JsonResponse({'status': 0, 'message': str(e)})

	def put(self, request, pk):
		try:
			product = Product.objects.get(pk=pk)
			if not product:
				return JsonResponse({'status': 0, 'message': 'There is a problem please try again'})
			name = request.data.get('name')
			user = request.user
			user = request.user
			if not (product.added_by == user):
				return JsonResponse({'status': 0, 'message': 'you dont have the previllage to update this product'})
			price = float(request.data.get('price'))
			category = request.data.get('categories')
			category = Category.objects.get(pk=category)
			if not category:
				return JsonResponse({'status': 0, 'message': 'There is a problem please try again'})
			description = request.data.get('description')
			stock = int(request.data.get('stock'))
			if stock == 0:
				available = False
			else:
				available = True
			unit = request.data.get('unit')
			if not user:
				return JsonResponse({'status': 0, 'message': 'There is a problem please try again'})
			try:
				product.name=name 
				product.price=price
				product.stock=stock
				product.available=available
				product.category=category
				product.description=description
				product.added_by=user
				product.save()
				return JsonResponse({'status': 1, 'message': 'product '+name+ ' has been updated successfully'})
			except Exception as e:
				return JsonResponse({'status': 0, 'message': str(e)})
		except Exception as e:
			return JsonResponse({'status': 0, 'message': str(e)})
		
class AdminViewCategory(generics.ListAPIView):
	permission_classes= (permissions.IsAuthenticatedOrReadOnly,)
	serializer_class = CategorySerializer
	queryset = Category.objects.all()

class AdminNewCategory(APIView):
	permission_classes= (permissions.IsAuthenticatedOrReadOnly,)
	serializer_class = CategorySerializer

	def post(self, request):
		try:
			name = request.data.get('name')
			cate = Category.objects.create(name=name)
			cate.save()
			return JsonResponse({'status': 1, 'message': 'category has been created successfully'})
		except Exception as e:
			return JsonResponse({'status': 0, 'message': str(e)})

class AdminUpdateCategory(generics.RetrieveUpdateDestroyAPIView):
	permission_classes= (permissions.IsAuthenticatedOrReadOnly,)
	serializer_class = CategorySerializer
	queryset = Category.objects.all()
	def delete(self, request, pk):
		try:
			category = Category.objects.get(pk=pk)
			if not category:
				return JsonResponse({'status': 0, 'message': 'Category Item Couldnt be found'})
			category.delete()
			return JsonResponse({'status': 1, 'message': 'Category has been deleted successfully'})
		except Exception as e:
			return JsonResponse({'status': 0, 'message': str(e)})

	def put(self, request, pk):
		try:
			category = Category.objects.get(pk=pk)
			if not category:
				return JsonResponse({'status': 0, 'message': 'Category Item Couldnt be found'})
			name = request.data.get('name')
			category.name = name
			category.save()
			return JsonResponse({'status': 1, 'message': 'category has been updated successfully'})
		except Exception as e:
			return JsonResponse({'status': 0, 'message': str(e)})
		


#Recently added products filterd by date
class RecentlyAdded(generics.ListAPIView):
	permission_classes= (permissions.IsAuthenticatedOrReadOnly,)
	serializer_class = ProductSerializer
	queryset = Product.objects.all().filter(available=True).order_by('name')

#product category list
class CategoryView(generics.ListAPIView):
	permission_classes= (permissions.IsAuthenticatedOrReadOnly,)
	serializer_class = CategorySerializer
	queryset = Category.objects.all().order_by('name')

#notification list

#notification manager either seen or not
class NotificationManager(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	serializer_class = ActionSerializer
	queryset = CustomerAction.objects.all()

	def get_notification(self, pk):
		try:
			return CustomerAction.objects.get(pk=pk)
		except:
			return None
	def put(self ,request, pk):
		notif = self.get_notification(pk)
		if not notif:
			return JsonResponse({'status': 0, 'message': 'something went wrong'})
		try:
			notif.seen = True
			notif.save()
			seen = str(notif.seen)
			return JsonResponse({'status': 1, 'message': 'Your Notifications marked as '+seen})
		except:
			return JsonResponse({'status': 0, 'message': 'something went wrong'})

#new Notification creater
def NewNotification(user, action, message):
	try:
		notif = CustomerAction.objects.create(user=user, action=action, message=message)
		notif.save()
		return True
	except Exception as e:
		print(str(e))
		return False


