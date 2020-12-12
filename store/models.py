"""Models for store"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    """A model representing a customer."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        """Return a string representation of the model."""
        return self.name


class Product(models.Model):
    """A model representing a product."""
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        """A decorator to fix for missing images url error while rendering index page."""
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Review(models.Model):
    """A model for reviews of a product."""
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    review = models.TextField()
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.review


class Order(models.Model):
    """A model representing an order/cart."""
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        """Whether shipping is required based on digital."""
        shipping = False
        order_items = self.orderitem_set.all()
        for item in order_items:
            if item.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        """Get total of all item's price in order/cart."""
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        """Get total number of items in order/cart."""
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    """A model representing an item in an order/cart."""
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name

    @property
    def get_total(self):
        """Return the total of our order."""
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    """A model representing a shipping address."""
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    
    class Meta:
        verbose_name_plural = "Shipping addresses"
        