from django.db import models

# Create your models here.
class Product(models.Model):
    """A model representing a product user can buy or sell."""
    name = models.CharField(max_length=200)
    date_added = models.DateField(auto_now_add=True)
    price = models.FloatField(default=0)

    def __str__(self):
        """Return a string representation of the model."""
        return self.name