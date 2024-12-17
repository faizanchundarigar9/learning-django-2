from django.urls import path
from django.shortcuts import render
from .models import Product, Reviews
from django.shortcuts import get_object_or_404

def home_view(request):
    products = Product.objects.all()
    return render(request,'home/home.html',{'products':products})

def reviews(request,pid):
    
    product = get_object_or_404(Product, pk=pid)
    reviews = Reviews.objects.filter(phone=product)
    return render(request, 'home/reviews.html',{'reveiws':reviews})

def details(request,pid):

    product = get_object_or_404(Product, pk=pid)
    return render(request, 'home/product_details.html',{'product':product})