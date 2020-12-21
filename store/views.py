"""Views page for store app."""
import json
import datetime

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, View
from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required

from .models import Product, Order, OrderItem, ShippingAddress, Review
from .utils import cart_data, guest_order
from .forms import ReviewForm, RegisterForm

# Create your views here.
def index(request):
    """The home page for our Ecom site."""
    data = cart_data(request)
    cart_items = data['cartItems']  

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cart_items}
    return render(request, 'store/index.html', context)


def view(request, product_id):
    """When user clicks view button for a particular item."""
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        # Take in the data the user submitted and save it as form
        form = ReviewForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():
            # Isolate the user review from the 'cleaned' version of form data
            review = form.cleaned_data['review']
            reviewer = request.user

            # See if the user has already given a review for the product
            try:
                # If so only edit the review
                edit_review = Review.objects.get(product=product, reviewer=reviewer)
                edit_review.review = review
                edit_review.save()
            except:
                # Else create a new review for the product with that user
                new_review = Review.objects.create(product=product, reviewer=reviewer, review=review)
                new_review.save()
            return HttpResponseRedirect(reverse('store:view', args=[product_id]))
    
    data = cart_data(request)
    items = data['items']
    cart_items = data['cartItems']
    form = ReviewForm()
    reviews = Review.objects.filter(product=product).all()
    for review in reviews:
        if review.reviewer == request.user:
            review = Review.objects.get(product=product, reviewer=request.user)
            form = ReviewForm(initial={'review': review})
    if len(reviews) == 1:
        reviews_count = "1 review"
    else:
        reviews_count = f"{len(reviews)} reviews"

    context = {
        'product': product,
        'items': items,
        'cartItems': cart_items,
        'form': form,
        'reviews': reviews,
        'reviews_count': reviews_count
        }
    return render(request, 'store/view.html', context)


def cart(request):
    """When user adds an item to cart."""
    data = cart_data(request)
    items = data['items']
    order = data['order']
    cart_items = data['cartItems']

    context = {'items': items, 'order': order, 'cartItems': cart_items}
    return render(request, 'store/cart.html', context)


def check_out(request):
    """When user wants to checkout cart items."""
    data = cart_data(request)
    items = data['items']
    order = data['order']
    cart_items = data['cartItems']

    context = {'items': items, 'order': order, 'cartItems': cart_items}
    return render(request, 'store/checkout.html', context)


def update_item(request):
    """Update item in cart."""
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']
    print('action:', action)
    print('prodcutId:', product_id)

    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(user=request.user, complete=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        order_item.quantity = (order_item.quantity + 1)
    elif action == 'remove':
        order_item.quantity = (order_item.quantity - 1)

    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse('Item was added', safe=False)


def process_order(request):
    """When user makes a payment."""
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
    else:
        user, order = guest_order(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            user= user,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode']
        )
    return JsonResponse('Payment complete!', safe=False)


def buy_now(request, product_id, qty):
    """When user clicks on 'buy now' button."""
    data = cart_data(request)
    cart_items = data['cartItems']

    product = Product.objects.get(id=product_id)
    # If product is digital, then shipping is False
    shipping = not product.digital
    total = product.price * int(qty)
    context = {
        'product': product,
        'shipping': shipping,
        'cartItems': cart_items,
        'qty': qty,
        'total': total
        }
    return render(request, 'store/buy_now.html', context)


def process_order_now(request):
    """When a user clicks 'buy now'."""
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        user = request.user
    else:
        # Creating a guest customer using the data received from the fetch API
        user, created = User.objects.get_or_create(username=data['form']['name'],email=data['form']['email'])
        user.save()

    order = Order(user=user, complete=True, transaction_id=transaction_id)
    order.save()
    
    # Check if we need to save shipping Info
    if data['shipping']['address'] != None:
        ShippingAddress.objects.create(
            user=user,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode']
        )
    return JsonResponse('Payment complete!', safe=False)


class ProductCreate(CreateView):
    """A create view to let users upload a product."""
    model = Product
    fields = ['name', 'price', 'digital', 'image', 'description']


def register(request):
    """A view to register new users."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('store:index')
    else:
        form = RegisterForm()
    
    return render(request, 'store/registration_form.html', {'form': form})


def profile(request):
    """Display user profile."""
    data = cart_data(request)
    cart_items = data['cartItems']
    return render(request, 'store/profile.html', {'cartItems': cart_items})