from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def home(request, slug=None):
    products = Product.objects.filter(available=True)
    categories = Category.objects.filter(is_sub=False)
    # scategory = Category.objects.filter(is_sub=True)
    if slug:
        category = get_object_or_404(Category, slug=slug)
        products = products.filter(category=category)
    return render(request, 'shop/home.html', {'products':products, 'categories':categories})


def product_details(request, id, slug):
    product = get_object_or_404(Product, pk=id, slug=slug)
    return render(request, 'shop/product_details.html', {'product':product})
