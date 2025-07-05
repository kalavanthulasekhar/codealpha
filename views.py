from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem
from .forms import SignUpForm
from decimal import Decimal

# helpers
def _get_cart(request):
    return request.session.setdefault('cart', {})

def _cart_items(request):
    cart = _get_cart(request)
    items = []
    for pid, qty in cart.items():
        product = get_object_or_404(Product, pk=pid)
        items.append({
            'product':  product,
            'quantity': qty,
            'subtotal': product.price * Decimal(qty),
        })
    return items

# product list & detail
def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

# cart operations
def add_to_cart(request, pk):
    cart = _get_cart(request)
    cart[str(pk)] = cart.get(str(pk), 0) + 1
    request.session.modified = True
    return redirect('cart')

def cart_view(request):
    items = _cart_items(request)
    total = sum(i['subtotal'] for i in items)
    return render(request, 'shop/cart.html', {'items': items, 'total': total})

def remove_from_cart(request, pk):
    cart = _get_cart(request)
    cart.pop(str(pk), None)
    request.session.modified = True
    return redirect('cart')

# checkout
@login_required
def checkout(request):
    items = _cart_items(request)
    if request.method == 'POST' and items:
        order = Order.objects.create(user=request.user, is_paid=True)
        for item in items:
            OrderItem.objects.create(
                order    = order,
                product  = item['product'],
                quantity = item['quantity']
            )
        request.session['cart'] = {}
        return render(request, 'shop/checkout.html', {'order': order, 'success': True})

    total = sum(i['subtotal'] for i in items)
    return render(request, 'shop/checkout.html', {'items': items, 'total': total})

# signup
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'shop/signup.html', {'form': form})
