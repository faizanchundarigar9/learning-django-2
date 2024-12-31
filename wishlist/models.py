from django.db import models
from django.contrib.auth.models import User
from home.models import Product

class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s wishlist"

class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.product.name} in {self.wishlist.user.username}'s wishlit"

