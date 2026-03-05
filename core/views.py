from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Order, OrderItem
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, F
from .models import Order, OrderItem
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator

@staff_member_required
@require_POST
def approve_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.status != 'pending':
        messages.warning(request, 'Đơn hàng này đã được xử lý.')
        return redirect('admin_dashboard')

    order.status = 'approved'
    order.save()

    messages.success(request, f'Đã duyệt đơn #{order.id}')
    return redirect('admin_dashboard')


@staff_member_required
@require_POST
def reject_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.status != 'pending':
        messages.warning(request, 'Đơn hàng này đã được xử lý.')
        return redirect('admin_dashboard')

    order.status = 'rejected'
    order.save()

    messages.error(request, f'Đã từ chối đơn #{order.id}')
    return redirect('admin_dashboard')

@staff_member_required
def approve_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 'approved'
    order.save()
    messages.success(request, f'Đã duyệt đơn #{order.id}')
    return redirect('admin_dashboard')


@staff_member_required
def reject_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 'rejected'
    order.save()
    messages.error(request, f'Đã từ chối đơn #{order.id}')
    return redirect('admin_dashboard')


@staff_member_required
def admin_dashboard(request):
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    approved_orders = Order.objects.filter(status='approved').count()
    rejected_orders = Order.objects.filter(status='rejected').count()

    total_revenue = OrderItem.objects.filter(
        order__status='approved'
    ).aggregate(total=Sum('price'))['total'] or 0

    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:5]

    return render(request, 'core/admin_dashboard.html', {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'approved_orders': approved_orders,
        'rejected_orders': rejected_orders,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
    })


def home(request):
    products = Product.objects.all()

    search = request.GET.get('search')
    sort = request.GET.get('sort')

    if search:
        products = products.filter(name__icontains=search)

    if sort == 'price_asc':
        products = products.order_by('price')

    if sort == 'price_desc':
        products = products.order_by('-price')

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)    

    return render(request, 'core/home.html', {'products': products})


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, 'Mật khẩu không khớp')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username đã tồn tại')
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        user.save()
        messages.success(request, 'Đăng ký thành công, hãy đăng nhập')
        return redirect('login')

    return render(request, 'core/register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Sai tài khoản hoặc mật khẩu')

    return render(request, 'core/login.html')


def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def place_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    order = Order.objects.create(
        user=request.user,
        status='pending'
    )

    OrderItem.objects.create(
        order=order,
        product=product,
        quantity=1,
        price=product.price
    )

    messages.success(request, 'Đặt hàng thành công! Đơn hàng đang chờ duyệt.')
    return redirect('home')

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/my_orders.html', {
        'orders': orders
    })

