# control method for funding an order
def PayPrice(user, amount):
	try:
		balance = user.balance
		user.balance = balance-amount
		user.save()
		return True
	except Exception as e:
		print(str(e))
		return False

# control method for refund on order delete
def Refund(user, amount):
	try:
		balance = user.balance
		user.balance = balance+amount
		user.save()
		return True
	except Exception as e:
		print(str(e))
		return False

# check if user has enough balance
def isBalanceSufficent(user, amount):
	if user.balance >= amount:
		return True
	elif user.balance < amount:
		return False

def ProductStockCheck(product, quantity):
	try:
		stock = product.stock
		if stock == 0:
			try:
				product.available = False
				product.save()
				return False
			except Exception as e:
				print(str(e))
				return False
		elif stock >= quantity:
			return True
		elif stock <= quantity:
			return False
	except Exception as e:
		print(str(e))
		return False

def ProductStockDeduct(product, quantity):
	try:
		stock = product.stock
		try:
			product.stock = stock - quantity
			product.save()
			return True
		except Exception as e:
			print(str(e))
			return False
	except Exception as e:
		print(str(e))
		return False

def ProductStockAdd(product, quantity):
	try:
		stock = product.stock
		try:
			product.stock = stock + quantity
			product.save()
			return True
		except Exception as e:
			print(str(e))
			return False
	except Exception as e:
		print(str(e))
		return False