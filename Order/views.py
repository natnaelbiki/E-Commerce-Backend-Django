from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import generics, permissions
from .serializers import OrderViewSerializer, OrderProductSerializer, OrderCreateSerializer, AdminOrderViewSerializer, OrderItemCreateSerializer
from accounts.models import CustomUser as User
from Product.models import Product
from .models import OrderProduct, BookOrder
from api.control import ProductStockCheck, Refund, PayPrice, ProductStockDeduct, ProductStockAdd, isBalanceSufficent
from Notification.models import CustomerAction, CustomerTransaction
from django.utils import timezone
import math

class AdminOrderView(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	serializer_class = AdminOrderViewSerializer
	
	def get(self, request):
		orders = OrderProduct.objects.all().order_by('-created_at')
		od_it = {}
		for x in orders:
			key = x.id
			order = str(x.order.user)
			price = str(x.price)
			product = str(x.product)
			status = str(x.status)
			created_at = x.created_at
			now = timezone.now()
			age = now - created_at
			if age.days == 0:
				if age.seconds < 3600:
					created_at = str(math.floor((age.seconds/60)))+" minute ago"
				elif age.seconds >= 3600:
					created_at = str(math.floor((age.seconds/60)/60))+" hours ago"
			else:
				if age.seconds < 3600:
					created_at = str(age.days)+' days ' + str(math.floor((age.seconds/60)))+" minute ago"
				elif age.seconds >= 3600:
					created_at = str(age.days)+' days ' + str(math.floor((age.seconds/60)/60))+" hours ago"

			if x.paid:
				paid = "Paid"
			else:
				paid = "Not Paid"
			it = {"id": x.id, 'order': order, "price": price, "quantity": x.quantity, 'created_at': created_at, "product": product, "status":status, "paid": paid}
			od_it.setdefault(key, it)
		return JsonResponse({'status':0,'message': 'all good', 'orders': od_it})

class AdminNewOrder(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	serializer_class = AdminOrderViewSerializer

	def post(self, request):
		try:
			uid = request.data.get('uid')
			user = User.objects.get(pk=uid)
			if not user:
				return JsonResponse({'status': 0, 'message': 'User couldnt be identified'})
			order = BookOrder.objects.get(user=user)
			if not order:
				return JsonResponse({'status': 0, 'message': 'Order couldnt be identified'})
			pid = request.data.get('product')
			product = Product.objects.get(pk=pid)
			if not product:
				return JsonResponse({'status': 0, 'message': 'Product couldnt be identified'})
			quantity = int(request.data.get('quantity'))
			price = product.price * quantity
			status = request.data.get('status')
			paid = request.data.get('paid')
			if paid == 'Paid':
				paid = True
			elif paid == 'Not Paid':
				paid = False
			ot = OrderProduct.objects.create(price=price, quantity=quantity, product=product, order=order, status=status, paid=paid)
			ot.save()
			return JsonResponse({'status': 1, 'message': 'product has been ordered successfully'})
		except Exception as e:
			return JsonResponse({'status': 0, 'message': str(e)})

class AdminUpdateOrder(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	serializer_class = AdminOrderViewSerializer
	queryset = OrderProduct.objects.all()
			
	def delete(self, request, pk):
		try:
			order = OrderProduct.objects.get(pk=pk)
			order.delete()
			return JsonResponse({'status': 1, 'message': 'Order has been deleted successfully'})
		except Exception as e:
			return JsonResponse({'status': 0, 'message': str(e)})


	def put(self, request, pk):
		try:
			order = OrderProduct.objects.get(pk=pk)
			if not order:
				return JsonResponse({'status': 0, 'message': 'order couldnt be identified'})
			quantity = int(request.data.get('quantity'))
			status = request.data.get('status')
			product = order.product
			order.quantity = quantity
			order.price = product.price * quantity
			order.status = status
			order.save()
			return JsonResponse({'status': 1, 'message': 'Order has been updated successfully'})
		except Exception as e:
			return JsonResponse({'status': 0, 'message': str(e)})
class DeliveryUpdateOrder(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	serializer_class = AdminOrderViewSerializer
	queryset = OrderProduct.objects.all()
			
	def delete(self, request, pk):
		try:
			order = OrderProduct.objects.get(pk=pk)
			order.delete()
			return JsonResponse({'status': 1, 'message': 'Order has been deleted successfully'})
		except Exception as e:
			return JsonResponse({'status': 0, 'message': str(e)})


	def put(self, request, pk):
		try:
			order = OrderProduct.objects.get(pk=pk)
			if not order:
				return JsonResponse({'status': 0, 'message': 'order couldnt be identified'})
			status = request.data.get('status')
			paid = request.data.get('paid')
			if paid == 'Paid':
				paid = True
			elif paid == 'Not Paid':
				paid = False
			order.status = status
			order.paid = paid
			order.save()
			return JsonResponse({'status': 1, 'message': 'Order has been updated successfully'})
		except Exception as e:
			return JsonResponse({'status': 0, 'message': str(e)})

class DeliveryOrderView(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	serializer_class = AdminOrderViewSerializer
	
	def get(self, request):
		orders = OrderProduct.objects.all()
		od_it = {}
		for x in orders:
			key = x.id
			order = str(x.order.user)
			owner = x.order
			user = owner.user
			address = {'region': str(user.region), 'zone': str(user.zone), 'city': str(user.city), 'kebelle': user.kebelle, 'Phone': user.Phone}
			price = str(x.price)
			product = str(x.product)
			status = str(x.status)
			created_at = x.created_at
			now = timezone.now()
			age = now - created_at
			if age.days == 0:
				if age.seconds < 3600:
					created_at = str(math.floor((age.seconds/60)))+" minute ago"
				elif age.seconds >= 3600:
					created_at = str(math.floor((age.seconds/60)/60))+" hours ago"
			else:
				if age.seconds < 3600:
					created_at = str(age.days)+' days ' + str(math.floor((age.seconds/60)))+" minute ago"
				elif age.seconds >= 3600:
					created_at = str(age.days)+' days ' + str(math.floor((age.seconds/60)/60))+" hours ago"

			if x.paid:
				paid = "Paid"
			else:
				paid = "Not Paid"
			it = {"id": x.id, 'order': order, "price": price, "quantity": x.quantity, 'created_at': created_at, "product": product, "status":status, "paid": paid, 'address': address}
			od_it.setdefault(key, it)
		return JsonResponse({'status':0,'message': 'all good', 'orders': od_it})	

class OrderView(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	serializer_class = OrderViewSerializer
	
	def get_user_object(self, pk):
		try:
			return User.objects.get(pk=pk)
		except:
			return None
	def get_order_object(self, user):
		try:
			return BookOrder.objects.get(user=user)
		except:
			return None
	def get_order_product(self, order):
		try:
			return OrderProduct.objects.all().filter(order=order)
		except:
			return None

	def post(self, request, format=None):
		uid = request.data.get('uid')
		user = self.get_user_object(uid)
		if not user:
			return JsonResponse({"status": 2, "message": "no such user"})
		order = self.get_order_object(user=user)
		if not order:	
			return JsonResponse({"status": 2, "message": "no such order"})
		serializer = OrderViewSerializer(order)
		items = self.get_order_product(order)
		if not items:
			return JsonResponse({"status": 1, "message": "Your Orders", "order": serializer.data})
		od_it = {}
		for x in items:
			key = x.id
			price = str(x.price)
			product = str(x.product)
			status = str(x.status)
			if x.paid:
				paid = "Paid"
			else:
				paid = "Not Paid"
			it = {"id": x.id, "price": price, "quantity": x.quantity, "product": product, "status":status, "paid": paid}
			od_it.setdefault(key, it)
		return JsonResponse({"status": 1, "message": "Your Orders and items", 'items':od_it, "order": serializer.data})

class OrderProductView(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	serializer_class = OrderProductSerializer

	def get_user_object(self, pk):
		try:
			return User.objects.get(pk=pk)
		except:
			return None
	
	def get_order_object(self, oid):
		try:
			return BookOrder.objects.get(id=oid)
		except:
			return None
	def get_order_product(self, order):
		try:
			return OrderProduct.objects.get(order=order)
		except:
			return None

	def post(self, request, format=None):
		oid = request.data.get('oid')
		order = self.get_order_object(oid)
		print(order.user)
		if not order:	
			return JsonResponse({"status": 2, "message": "no such order"})
		items = self.get_order_product(order)
		if not items:
			return JsonResponse({"status": 2, "message": "no orders yet"})
		print(items)
		od_it = {}
		for x in items:
			key = x.id
			price = float(x.price)
			product = str(x.product)
			status = str(x.status)
			if x.paid:
				paid = "Paid"
			else:
				paid = "Not Paid"
			it = {"id": x.id, "price": price, "quantity": x.quantity, "product": product, "status":status, "paid": paid}
			od_it.setdefault(key, it)
			#print(it)
		return JsonResponse({"status": 1, "message": "Your Ordered Items", "items": od_it})


class OrderCreate(generics.CreateAPIView):
	permission_classes= (permissions.IsAuthenticated,)
	serializer_class = OrderCreateSerializer

	def get_object(self, pk):
		try:
			return User.objects.get(pk=pk)
		except:
			return None
	def get_order_object(self, user):
		try:
			return BookOrder.objects.get(user=user)
		except:
			return None
	def get_user(self, pk):
		try:
			return User.objects.get(pk=pk)
		except:
			return None

	def get_user_object(self, pk):
		try:
			return User.objects.get(pk=pk)
		except:
			return None

	def post(self, request, format=None):
		uid = request.data.get('uid')
		user = self.get_user_object(uid)
		ordered = self.get_order_object(user)
		if not ordered:
			try:
				order = BookOrder.objects.create(user=user)
				return JsonResponse({"status": 1, "message":"order saved successfully","orderid": order.id})
			except:
				return JsonResponse({"status": 2, "message":"Order cant be saved"})
		return JsonResponse({"status": 1, "message":"order saved successfully","orderid": ordered.id})




class OrderItemCreate(generics.CreateAPIView):
	permission_classes= (permissions.IsAuthenticated,)
	serializer_class = OrderItemCreateSerializer

	def get_user(self, pk):
		try:
			return User.objects.get(pk=pk)
		except:
			return None
	def get_order(self, oid):
		try:
			return BookOrder.objects.get(id=oid)
		except:
			return None
	def get_product(self, pid):
		try:
			return Product.objects.get(id=pid)
		except:
			return None

	def post(self, request, format=None):
		method = request.data.get('method')
		if method == 'item':
			uid = request.data.get('uid')
			oid = request.data.get('order')
			pid = request.data.get('product')
			quantity = int(request.data.get('quantity'))
			user = self.get_user(uid)
			if not user:
				return JsonResponse({"status": 2,"message":"The Product cant be ordered because user is not found"})
			order = self.get_order(oid)
			if not order:
				return JsonResponse({"status": 2,"message":"The Product cant be ordered because user is not found"})
			product = self.get_product(pid)
			if not product:
				return JsonResponse({"status": 2,"message":"The Product cant be ordered because user is not found"})
			price = product.price * quantity
			previous = user.balance
			if ProductStockCheck(product, quantity):
				if isBalanceSufficent(user, price):
					if OrderItem(user, order, product, quantity):
						if ProductStockDeduct(product, quantity):
							try:
								name = product.name
								trans = {action: 'Payment', price: price, balance: user.balance}
								NewTransaction(user, 'Payment', price, previous, user.balance)
								NewNotification(user, 'Product Ordered', name+' has been ordered successfully')
								return JsonResponse({"status": 1,"message":"Your Product has been ordered successfully","orderid": oid, 'trans': trans})
							except Exception as e:
								return JsonResponse({"status": 2,"message":"The Product cant be ordered because"+str(e)})
						else:
							return JsonResponse({"status": 2,"message":"Your Product cant be ordered because stock is not sufficent"})
					else:
						return JsonResponse({"status": 2,"message":"Your Product cant be ordered! something went wrong"})
				else:
					return JsonResponse({"status": 2,"message":"Your Product cant be ordered because your balance is not sufficent"})
		elif method == 'cart':
			uid = request.data.get('uid')
			oid = request.data.get('order')
			total = request.data.get('total')
			user = self.get_user(uid)
			if not user:
				return JsonResponse({"status": 2,"message":"Your Cart cant be ordered because user is not found"})
			order = self.get_order(oid)
			if not order:
				return JsonResponse({"status": 2,"message":"Your Cart cant be ordered because user is not found"})
			items = request.data.get('item')
			name = ''
			previous = user.balance
			if isBalanceSufficent(user, total):
				for x in items:
					quantity = x['count']
					product = self.get_product(x['id'])
					if not product:
						return JsonResponse({"status": 2,"message":"The Product cant be ordered because user is not found"})
					price = product.price * quantity
					if ProductStockCheck(product, quantity):
						if OrderItem(user, order, product, quantity):
							if ProductStockDeduct(product, quantity):
								try:
									if name == '':
										name = product.name
									elif name != '':
										name = name + ', and '+product.name
								except Exception as e:
									print(e)
							else:
								return JsonResponse({"status": 2,"message":"Your Product cant be ordered because stock is not sufficent"})
					else:
						return JsonResponse({"status": 2,"message":"Your Product cant be ordered because stock is not sufficent"})
					NewTransaction(user, 'Payment-Cart', price, previous, user.balance)
				NewNotification(user, 'Cart Ordered', name+' has been ordered successfully')
				return JsonResponse({"status": 1,"message":"Your Product has been ordered successfully","orderid": order.id})
			else:
				return JsonResponse({"status": 2,"message":"The Cart cant be ordered because your balance is not sufficent"})


class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = OrderProductSerializer

	def get_queryset(self):
		return OrderProduct.objects.all()

	def get(self, request, pk):
		try:
			item = OrderProduct.objects.get(pk=pk)
			serializer = OrderProductSerializer(item)
			return JsonResponse({'status': 1, 'message': 'your order','item': serializer.data})
		except:
			return JsonResponse({'status': 0, 'message': 'no such order'})

	def put(self, request, pk):
		item = OrderProduct.objects.get(pk=pk)
		if not item:
			return JsonResponse({'status': 0, 'message': 'no such order'})
		order = item.order
		user = order.user
		previous = user.balance
		product = item.product
		quantity = item.quantity
		amount = product.price * quantity
		if Refund(user, amount):
			NewTransaction(user, 'Refund', amount, previous, user.balance)
			if ProductStockAdd(product, quantity):
				new_quantity = int(request.data.get('quantity'))
				amount = product.price * new_quantity
				previous = user.balance
				if PayPrice(user, amount):
					if ProductStockDeduct(product, new_quantity):
						item.quantity = new_quantity
						item.price = product.price * new_quantity
						item.save()
						serializer = OrderProductSerializer(item)
						NewTransaction(user, 'Payment', amount, previous, user.balance)
						NewNotification(user=user, action="Order Changed", message='Order Changed successfully')
						return JsonResponse({'status': 1, 'message': 'Order Updated successful', 'item': serializer.data})
		else:
			return JsonResponse({'status': 0, 'message': 'action not successful please try again later!'})


	def delete(self, request, pk):
		item = OrderProduct.objects.get(pk=pk)
		price = float(item.price)
		quantity = item.quantity
		order = item.order
		user = order.user
		previous = user.balance
		product = item.product
		amount = product.price * quantity
		if Refund(user, amount):
			if ProductStockAdd(product, quantity):
				item.delete()
				NewTransaction(user, 'Refund', amount, previous, user.balance)
				NewNotification(user=user, action="Order Delete", message='Order deleted successfully')
				return JsonResponse({'status': 1, 'message': 'action successful'})
		else:
			return JsonResponse({'status': 0, 'message': 'action not successful please try again later!'})
#Notifier
def NewNotification(user, action, message):
	try:
		notif = CustomerAction.objects.create(user=user, action=action, message=message)
		notif.save()
		return True
	except Exception as e:
		print(str(e))
		return False

def NewTransaction(user, action, amount, previous, current):
	try:
		trans = CustomerTransaction.objects.create(user=user, action=action, amount=amount, previous_balance=previous, current_balance = current)
		trans.save()
		return True
	except Exception as e:
		print(str(e))
		return False
#order method
def OrderItem(user, order, product, quantity):
	try:
		price = product.price * quantity
		if isBalanceSufficent(user, price):
			try:
				if PayPrice(user, price):
					ot = OrderProduct.objects.create(price=price, quantity=quantity, product=product, order=order, status="ordered", paid=True)
					ot.save()
					return True
				else:
					return False
			except:
				return False
		else:
			return False
	except Exception as e:
		print(str(e))
		return False

# Create your views here.
