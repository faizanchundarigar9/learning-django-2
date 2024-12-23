from django.urls import path
from django.shortcuts import render, redirect
from .models import Product, Reviews, Category
from django.shortcuts import get_object_or_404
from .forms import InputForm
from django.contrib.auth import authenticate, login

def home_view(request):
    categories = Category.objects.all()
    return render(request,'home/home.html',{'categories':categories})

def view_products_by_category(request,cid):
    products = Product.objects.all().filter(category_id = cid)
    return render(request, 'home/products.html', {'products':products})

def reviews(request,pid):
    
    product = get_object_or_404(Product, pk=pid)
    reviews = Reviews.objects.filter(phone=product)
    return render(request, 'home/reviews.html',{'reveiws':reviews})

def details(request,pid):

    product = get_object_or_404(Product, pk = pid)
    return render(request, 'home/product_details.html',{'product':product})

def search_result(request):
    
    searchterm = request.GET.get('searchterm', '')
    products = Product.objects.filter(name__contains = searchterm)
    return render(request, 'home/products.html',{'products' : products})

def login_view(request):
    
    if request == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('smart-phone')
        
        else:
            return render(request,'home/login.html', {'error': 'Invalid credentials.'})

    else:
        return render(request, 'home/login.html')  

def cart_view(reuqest):
    return render(reuqest,'home/cart.html')    
    


 