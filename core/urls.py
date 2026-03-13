from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

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
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order-detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='core/change_password.html'), name='change_password'),
    path('change-password-done/', auth_views.PasswordChangeDoneView.as_view(template_name='core/change_password_done.html'), name='password_change_done'),
    
]