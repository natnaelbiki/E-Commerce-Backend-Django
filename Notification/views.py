from rest_framework import generics, permissions
from rest_framework.views import APIView
from django.http import JsonResponse
from django.shortcuts import render
from .models import CustomerAction, CustomerTransaction
from .serializers import ActionSerializer, TransactionSerializer
from accounts.models import CustomUser as User
from django.utils import timezone
import math


class ActionView(generics.ListAPIView):
	permission_classes = [permissions.IsAuthenticated,]
	serializer_class = ActionSerializer

	def get_queryset(self):
		user =self.request.user
		actions = CustomerAction.objects.filter(user=user)
		for x in actions:
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
			x.age = created_at
			x.save()
		return actions

	



class TransactionView(generics.ListAPIView):
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = TransactionSerializer

	def get_queryset(self):
		user =self.request.user
		transaction = CustomerTransaction.objects.filter(user=user)
		for x in transaction:
			created_at = x.created_at
			print(created_at)
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
			x.age = created_at
			x.save()
			print(x.created_at)
		return transaction
# Create your views here.
