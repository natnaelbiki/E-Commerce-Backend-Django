uid = request.data.get("uid")
		user = self.get_user(uid)
		if not user:
			return JsonResponse({"status": 2,"message":"The Product cant be ordered because user is not found"})
		quantity = int(request.data.get('quantity'))
		order_id = request.data.get('order')
		order = self.get_order(order_id)
		if not order:
			return JsonResponse({"status": 2,"message":"The Product cant be ordered because order is not found"})
		product_id = request.data.get('product')
		product = Product.objects.get(id=product_id)
		if not product:
			return JsonResponse({"status": 2,"message":"The Product cant be ordered because product is not found"})
		price = product.price
		if not product.available:
			return JsonResponse({"status": 2,"message":"The Product cant be ordered because product is not available"})
		balance = user.balance
		stock = product.stock
		if stock == 0:
			product.available = False
			product.save()
			return JsonResponse({"status": 2,"message":"The Product cant be ordered because product is not in stock"})
		product.stock = stock - quantity
		product.save()
		amount = price * quantity
		if balance >= amount:
			if OrderItem(user, order, product, quantity):
				NewNotification(user=user, action='Product Ordered', message=name+' has been ordered successfully')
				return JsonResponse({"status": 1,"message":"The Product has been ordered successfully","orderid": order_id})
		elif balance<amount:
			return JsonResponse({"status": 2,"message":"The Product cant be ordered because your balance is not sufficent"})
		try:
			name = product.name
			#orderItem = OrderProduct.objects.create(price=price*quantity, quantity=quantity, product=product, order=order, status="ordered", paid=True)
			#orderItem.save()
			NewNotification(user=user, action='Product Ordered', message=name+' has been ordered successfully')
			return JsonResponse({"status": 1,"message":"The Product has been ordered successfully","orderid": order_id})
		except:
			return JsonResponse({"status": 2,"message":"The Product cant be ordered please try again"})
		