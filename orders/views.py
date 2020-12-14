from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Order, OrderItem, Copoun
from cart.cart import Cart
from suds.client import Client
from django.http import HttpResponse
from django.contrib import messages
from .forms import CopounForm
from django.utils import timezone

@login_required
def order_create(request):
    cart = Cart(request)
    order = Order.objects.create(user=request.user)
    for item in cart:
        OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
        cart.clear()
    return redirect('orders:details', order.id)


@login_required
def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    form = CopounForm()
    return render(request, 'orders/details.html', {'order':order, 'form':form})


MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
CallbackURL = 'http://localhost:8000/orders/verify/' # Important: need to edit for realy server.


@login_required
def payment(request, order_id, price):
    global amount, o_id
    amount = price
    o_id = order_id
    result = client.service.PaymentRequest(MERCHANT, amount, description, request.user.email, CallbackURL)
    if result.Status == 100:
        return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
    else:
        return HttpResponse('Error code: ' + str(result.Status))


@login_required
def verify(request):
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        if result.Status == 100:
            order = Order.objects.get(id=order_id)
            order.paid = True
            messages.success(request, 'your paid wad successful', 'success')
            return redirect('shop:home')
        elif result.Status == 101:
            return HttpResponse('Transaction submitted : ' + str(result.Status))
        else:
            return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
    else:
        return HttpResponse('Transaction failed or canceled by user')


@require_POST
def copoun_apply(request, order_id):
    now = timezone.now()
    form = CopounForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            copoun = Copoun.objects.get(code__iexact=code, valid_from__lte=now, valid_to__gte=now)
            order = Order.objects.get(id=order_id)
            order.discount = copoun.percent
            order.save()
            return redirect('orders:details', order_id)
        except copoun.DoesNotExist:
            messages.error(request, 'Copoun dose not exsit', 'danger')
            return redirect('orders:details', order_id)
    return redirect('orders:details', order_id)
