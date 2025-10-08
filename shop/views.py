# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order
from django.contrib import messages
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Order

from decimal import Decimal, ROUND_HALF_UP


from django.db.models import Sum
from .models import Product, Order  # ✅ Make sure these imports exist

from django.db.models import Sum, F, FloatField
from django.db.models.functions import Coalesce

@login_required
def dashboard(request):
    products = Product.objects.all().order_by('-created_at')
    orders = Order.objects.all()

    total_products = products.count()
    total_orders = orders.count()

    # 💡 Calculate total revenue dynamically
    total_revenue = orders.aggregate(
        total=Coalesce(Sum(F('product__price') * F('quantity'), output_field=FloatField()), 0.0)
    )['total']

    context = {
        'products': products,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
    }

    return render(request, 'shop/dashboard.html', context)

def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'shop/product_list.html', {'products': products})

def place_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        quantity = int(request.POST.get('quantity', 1))
        Order.objects.create(
            product=product,
            quantity=quantity,
            customer_name=name,
            customer_email=email,
            shipping_address=address
        )
        messages.success(request, f'Your order for {product.name} was placed successfully!')
        return redirect('product_list')

    return render(request, 'shop/place_order.html', {'product': product})

from django.contrib.auth.decorators import login_required
from django import forms

# Product form for Create & Edit
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('dashboard')
    else:
        form = ProductForm()
    return render(request, 'shop/add_product.html', {'form': form})

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'shop/edit_product.html', {'form': form, 'product': product})

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, 'Product deleted successfully!')
    return redirect('dashboard')


@login_required
def order_list(request):
    orders = Order.objects.select_related('product').order_by('-created_at')

    total_revenue = Decimal('0.00')
    total_tax = Decimal('0.00')

    # Compute per-order totals
    for o in orders:
        # Ensure product price and quantity exist
        price = Decimal(o.product.price)
        qty = Decimal(o.quantity)

        o.subtotal = (price * qty).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        o.tax = (o.subtotal * Decimal('0.18')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        o.total = (o.subtotal + o.tax).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        total_revenue += o.total
        total_tax += o.tax

    # ✅ Make sure we pass all these to the template
    context = {
        'orders': orders,
        'total_revenue': total_revenue,
        'total_tax': total_tax,
    }

    return render(request, 'shop/order_list.html', context)
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

@login_required
def delete_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.delete()
    messages.success(request, "Order deleted successfully!")
    return redirect('order_list')