from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST

from django.db.models import Sum, F
from django.db.models.functions import TruncMonth
from django.core.paginator import Paginator

from .models import Product, Order, OrderItem, UserProfile

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
        phone = request.POST['phone']
        address = request.POST['address']
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

        UserProfile.objects.create(
            user=user,
            phone=phone,
            address=address
        )
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
    payment_method = request.POST.get("payment_method")

    order = Order.objects.create(
    user=request.user,
    status='pending',
    payment_method=payment_method
)

    order_item = OrderItem.objects.create(
        order=order,
        product=product,
        quantity=1,
        price=product.price
)

    order.total_price = order_item.price * order_item.quantity
    order.save()

    messages.success(request, 'Đặt hàng thành công! Đơn hàng đang chờ duyệt.')
    return redirect('home')

@login_required
def order_detail(request, order_id):

    order = get_object_or_404(Order, id=order_id, user=request.user)

    return render(request, 'core/order_detail.html', {
        'order': order
    })

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/my_orders.html', {
        'orders': orders
    })

def admin_dashboard(request):

    total_orders = Order.objects.count()

    total_revenue = Order.objects.filter(status='approved').aggregate(
    total=Sum('total_price')
)['total'] or 0

    pending_count = Order.objects.filter(status='pending').count()
    approved_count = Order.objects.filter(status='approved').count()
    rejected_count = Order.objects.filter(status='rejected').count()

    orders = Order.objects.order_by('-created_at')[:10]

    revenue_by_month = (
        Order.objects.filter(status='approved')
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=Sum('total_price'))
        .order_by('month')
    )

    months = []
    revenues = []

    for item in revenue_by_month:
        months.append(item['month'].strftime("%m-%Y"))
        revenues.append(float(item['total']))

    top_products = (
        OrderItem.objects
        .values('product__name')
        .annotate(total_sold=Sum('quantity'))
        .order_by('-total_sold')[:5]

)

    product_names = []
    product_sales = []

    for item in top_products:
        product_names.append(item['product__name'])
        product_sales.append(item['total_sold'])

    context = {
        "orders": orders,

        "total_orders": total_orders,
        "total_revenue": total_revenue,

        "pending": pending_count,
        "approved": approved_count,
        "rejected": rejected_count,

        "months": months,
        "revenues": revenues,

        "product_names": product_names,
        "product_sales": product_sales,
}

    return render(request, "core/admin_dashboard.html", context)