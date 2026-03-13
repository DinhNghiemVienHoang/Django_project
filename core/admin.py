from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Category, Product, Order, OrderItem
from django.contrib.auth.models import User, Group
from .models import UserProfile

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
    search_fields = ('user__username',)
    actions = [approve_orders, reject_orders]

class MyAdminSite(AdminSite):
    site_header = "Flower Shop Administration"
    site_title = "Flower Shop Admin"
    index_title = "Welcome to Flower Shop"

    class Media:
        css = {
            "all": ("admin/custom.css",)
        }

admin_site = MyAdminSite(name="myadmin")

admin_site.register(Category)
admin_site.register(Product)
admin_site.register(Order)
admin_site.register(OrderItem)

admin_site.register(User)
admin_site.register(Group)
admin_site.register(UserProfile)