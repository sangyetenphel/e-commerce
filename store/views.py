"""Views page for store app."""

from django.shortcuts import render

from .models import Product

# Create your views here.
def index(request):
    """The home page for our Ecom site."""
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/index.html', context)
