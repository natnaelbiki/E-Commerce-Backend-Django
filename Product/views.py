from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import generics, permissions
from accounts.models import CustomUser as User
from Product.models import Product
from .models import OrderProduct, BookOrder
from api.control import ProductStockCheck, Refund, PayPrice, ProductStockDeduct, ProductStockAdd, isBalanceSufficent
from Notification.models import CustomerAction, CustomerTransaction
from django.utils import timezone
import math




