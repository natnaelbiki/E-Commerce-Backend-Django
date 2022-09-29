from django.db import models
from accounts.models import CustomUser as User
from Product.models import Product

Order_Status = {("pending", "Pending"), ("ordered", "Ordered"), ("delivered", "Delivered")}



class BookOrder(models.Model):
	user = models.OneToOneField(User, related_name="owner", on_delete=models.CASCADE)
	
class OrderProduct(models.Model):
	order = models.ForeignKey(BookOrder, null=False, related_name='order', on_delete=models.CASCADE)
	product = models.ForeignKey(Product,null=False, on_delete=models.CASCADE)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	quantity = models.PositiveIntegerField(default=1)
	paid = models.BooleanField(default=False)
	status = models.CharField(max_length=30, choices=Order_Status,default="pending")
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('-created_at',)

	def __str__(self):
		return '{}'.format(self.id)

	def get_cost(self):
		return self.price * self.quantity
# Create your models here.
