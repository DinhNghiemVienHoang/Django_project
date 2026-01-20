from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('order/<int:product_id>/', views.place_order, name='place_order'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/orders/<int:order_id>/approve/', views.approve_order, name='approve_order'),
    path('dashboard/orders/<int:order_id>/reject/', views.reject_order, name='reject_order'),
    path('orders/<int:order_id>/approve/', views.approve_order, name='approve_order'),
    path('orders/<int:order_id>/reject/', views.reject_order, name='reject_order'),

]