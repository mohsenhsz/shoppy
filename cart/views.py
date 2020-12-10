from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product
from .forms import CartAddForm
from .cart import Cart
from django.views.decorators.http import require_POST


def details(request):
    cart = Cart(request)
    return render(request, 'cart/details.html', {'cart':cart})


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    form = CartAddForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product, cd['quantity'])
    return redirect('cart:details')


def remove(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.remove(product)
    return redirect('cart:details')
