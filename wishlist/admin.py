from django.contrib import admin
from .models import Wishlist, WishlistItem

class CustomWishlist(admin.ModelAdmin):
    list_display = ('id','user')

class CustomWishlistItem(admin.ModelAdmin):
    list_display = ('id','product') 

admin.site.register(WishlistItem,CustomWishlistItem)
admin.site.register(Wishlist,CustomWishlist)
