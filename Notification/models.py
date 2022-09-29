from django.db import models
from accounts.models import CustomUser as User


class CustomerAction(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	action = models.CharField(max_length=25, null=False, default='Action')
	message = models.CharField(max_length=200, null=False)
	created_at = models.DateTimeField(auto_now_add=True)
	age = models.CharField(max_length=25, null=True)
	seen = models.BooleanField(default=False)

	class Meta:
		ordering = ('-created_at',)
	
	def __str__(self):
		return str(self.user)+" "+self.action


class CustomerTransaction(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	action = models.CharField(max_length=25, null=False, default='Action')
	amount = models.PositiveIntegerField()
	previous_balance = models.PositiveIntegerField()
	current_balance = models.PositiveIntegerField()
	created_at = models.DateTimeField(auto_now_add=True)
	age = models.CharField(max_length=25, null=True)
	seen = models.BooleanField(default=False)


	def __str__(self):
		return str(self.action)

	class Meta:
		ordering = ('-created_at',)