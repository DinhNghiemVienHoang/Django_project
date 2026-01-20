from django.contrib import admin
from .models import Category, Product, Order, OrderItem

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(OrderItem)

@admin.action(description="✔ Duyệt đơn hàng")
def approve_orders(modeladmin, request, queryset):
    queryset.update(status='approved')

@admin.action(description="✖ Từ chối đơn hàng")
def reject_orders(modeladmin, request, queryset):
    queryset.update(status='rejected')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    actions = [approve_orders, reject_orders]