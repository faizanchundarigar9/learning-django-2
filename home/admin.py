from django.contrib import admin
from .models import Product, Reviews, Category, Cart, CartProduct
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Reviews)
admin.site.register(Cart)
admin.site.register(CartProduct)



