"""Models for store"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    """A model representing a product user can buy or sell."""
    date_added = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=200)
    price = models.FloatField()
    quantity = models.IntegerField(default=1)

    def __str__(self):
        """Return a string representation of the model."""
        return self.name


class Cart(models.Model):
    """A cart to store user items."""
    date_added = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.item} (Qty - {self.quantity})"