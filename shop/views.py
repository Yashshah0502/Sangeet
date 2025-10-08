# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order
from django.contrib import messages

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
def dashboard(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'shop/dashboard.html', {'products': products})

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
