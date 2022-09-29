from django.urls import path,include
from . import views
from simple_chatbot.views import SimpleChatbot, chatbot, AdminViewTag, AdminViewUserMessage, AdminViewTokens
from Order.views import OrderView, AdminNewOrder, AdminUpdateOrder, OrderProductView, DeliveryUpdateOrder, DeliveryOrderView, OrderCreate, OrderItemCreate, OrderDetail, AdminOrderView
from accounts.views import login, AdminUserDetail, AdminNewUser, AdminUpdateUser, signup, UserDetail, UserProfile, UserEditDetail, UserChangePassword
from Notification.views import ActionView, TransactionView

urlpatterns = [
	#admin urls
	
	#products
	path('adminViewProducts/', views.AdminViewProducts.as_view()),
	path('adminAddNewProducts/', views.AdminAddNewProducts.as_view()),
	path('adminUpdateProduct/<int:pk>', views.AdminUpdateProduct.as_view()),

	#category
	path('adminViewCategory/', views.AdminViewCategory.as_view()),
	path('adminAddCategory/', views.AdminNewCategory.as_view()),
	path('adminUpdateCategory/<int:pk>', views.AdminUpdateCategory.as_view()),

	#order
	path('adminOrderView/', AdminOrderView.as_view()),
	path('adminNewOrder/', AdminNewOrder.as_view()),
	path('adminUpdateOrder/<int:pk>', AdminUpdateOrder.as_view()),

	#chatbot
	path('adminUserView/', AdminUserDetail.as_view()),
	path('adminNewUser/', AdminNewUser.as_view()),
	path('adminUpdateUser/<int:pk>', AdminUpdateUser.as_view()),

	#chatbot
	path('adminTagView/', AdminViewTag.as_view()),
	path('adminTokenView/', AdminViewTokens.as_view()),
	path('adminUserMessageView/', AdminViewUserMessage.as_view()),
	
	
	
	#supplier views
	path('supplierViewProducts/', views.SupplierViewProducts.as_view()),
	path('supplierAddNewProducts/', views.SupplierAddNewProducts.as_view()),
	path('supplierUpdateProduct/<int:pk>', views.SupplierUpdateProduct.as_view()),

	#delivery views
	path('deliveryViewOrders/', DeliveryOrderView.as_view()),
	path('deliveryUpdateOrder/<int:pk>', DeliveryUpdateOrder.as_view()),
	
	#Shop urls
	path('',views.Home.as_view()),
	path('recent',views.RecentlyAdded.as_view()),
	path('category/', views.CategoryView.as_view()),
	
	#Chatbot urls
	path("chatbot/", SimpleChatbot.as_view()),
	path('chatbott/', chatbot),#for unauthenticated user's
	
	#User Account urls
	path('login/', login),
	path('signup/', signup),
	path('user/<int:pk>',UserDetail.as_view()),
	path('userprofile/',UserProfile.as_view()),
	path('usereditprofile/<int:pk>', UserEditDetail.as_view()),
	path('changepassword/', UserChangePassword.as_view()),
	
	#Order urls
	path('orders/', OrderView.as_view()),
	path('ordereditems/<int:pk>', OrderDetail.as_view()),
	path('ordereditems/', OrderProductView.as_view()),
	path('neworder/', OrderCreate.as_view()),
	path('neworderitem/', OrderItemCreate.as_view()),
	
	#Notification urls
	path('notification/', ActionView.as_view()),
	path('transaction/', TransactionView.as_view()),
	path('notification/<int:pk>', views.NotificationManager.as_view()),
	]