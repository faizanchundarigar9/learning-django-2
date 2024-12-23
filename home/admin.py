from django.contrib import admin
from .models import Product, Reviews, User, Cart, Category

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Reviews)
admin.site.register(User)
admin.site.register(Cart)