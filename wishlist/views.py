from django.shortcuts import render
from .models import Wishlist, WishlistItem
from django.shortcuts import redirect
from home.models import Product
from django.contrib import messages



from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import WishlistItem
from .serializers import WishlistItemSerializer


def view_wishlist(request):
    
    wishlist, created = Wishlist.objects.get_or_create(user = request.user)
    wishlist_items = WishlistItem.objects.all().filter(wishlist = wishlist)

    return render(request,'wishlist/view_wishlist.html',context = {'wishlist_items':wishlist_items})

def remove_product_from_wishlist(request,wishlist_item_id):

    wishlist_product = WishlistItem.objects.get(id = wishlist_item_id)
    wishlist_product.delete()

    messages.warning(request,"Product removed from wishlist ☹️") 
    return redirect('view_wishlist')

def add_to_wishlist(request,pid):
    
    users_wish_list, created = Wishlist.objects.get_or_create(user = request.user)
    product_added = Product.objects.get(id = pid)

    wishlist_product,created  = WishlistItem.objects.get_or_create(wishlist = users_wish_list, product = product_added)

    if created:
        messages.warning(request, "Product added to wishlist 🤩")
        wishlist_product.save()
    
    else:
        messages.warning(request, "Product is already in your wishlist 🤩")
    
    return redirect('smart-phone')

# API view to fetch wishlist items for the logged-in user
# @api_view(['GET'])
# def get_wishlist_items(request):
#     if request.user.is_authenticated:
#         wishlist_items = WishlistItem.objects.filter(wishlist__user=request.user)
#         serializer = WishlistItemSerializer(wishlist_items, many=True)
#         return Response(serializer.data)
#     return Response({"detail": "Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)


