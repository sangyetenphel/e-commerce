"""Views page for store app."""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Product, Cart

# Create your views here.
def index(request):
    """The home page for our Ecom site."""
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/index.html', context)


@login_required
def cart(request):
    """When user adds an item to cart"""
    cart = Cart.objects.filter(user=request.user).order_by('date_added')
    context = {'cart': cart }
    return render(request, 'store/cart.html', context)


def add_cart(request, product_id):
    return redirect('store:index')

