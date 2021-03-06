"""Helper module for views"""
import json
from django.contrib.auth.models import User
from . models import Product, Order, OrderItem


def cookie_cart(request):
    """Generate cart for unauthorized user."""
    try:
        # Coverting into a python dictionary the cookie 'cart' from our site browser
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    items = []
    order = {'get_cart_items':0, 'get_cart_total':0, 'shipping':False}
    cart_items = order['get_cart_items']

    for product_id in cart:
        try:
            cart_items += cart[product_id]['quantity']

            product = Product.objects.get(id=product_id)
            total = product.price * cart[product_id]['quantity']

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[product_id]['quantity']

            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'image_url':product.image_url
                },
                'quantity':cart[product_id]['quantity'],
                'get_total':total
            }
            items.append(item)

            if product.digital == False:
                order['shipping']  = True
        except:
            pass
    return {'items': items, 'order': order, 'cartItems': cart_items}


def cart_data(request):
    """Generate the items, orders, cartItems based on user authentication."""
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        cookie_data = cookie_cart(request)
        items = cookie_data['items']
        order = cookie_data['order']
        cart_items = cookie_data['cartItems']
    return {'items': items, 'order': order, 'cartItems': cart_items}


def guest_order(request, data):
    """Return a guest as a customer and his orders."""
    name = data['form']['name']
    email = data['form']['email']

    cookie_data = cookie_cart(request)
    items = cookie_data['items']

    # We will create an account for unauthorized user with their email just incase for keeping track
    user, created = User.objects.get_or_create(
        email=email
    )
    user.username = name
    user.save()

    order = Order.objects.create(
        user=user,
        complete=False,
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        order_item = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )
    return user, order
