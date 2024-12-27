from django.urls import path
from django.shortcuts import render, redirect
from .models import Product, Reviews, Category
from django.shortcuts import get_object_or_404
from .forms import InputForm
from django.contrib.auth import authenticate, login, get_user_model
from home.models import Cart, CartProduct



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

    if request.method == 'POST':
        print("post request received")
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(f"Username: {username}, Password: {password}")

        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('smart-phone')
        
        else:
            return render(request,'home/index.html', {'error': 'Invalid credentials.'})

    else:
        print("GET request received")
        return render(request, 'home/index.html')  

def cart_view(request):
    # Fetch the cart for the logged-in user
    cart = Cart.objects.get(user=request.user)
    cart_products = CartProduct.objects.filter(cart=cart)
    context = {
        'cart': cart,
        'cart_products': cart_products,
    }
    return render(request, 'home/cart.html', context)

def add_to_cart(request, product_id):
    # Get the quantity from the request (default to 1)
    quantity = int(request.GET.get('quantity', 1))
    
    if quantity <= 0:
        # Invalid quantity
        return redirect('product_list')

    try:
        product = Product.objects.get(id=product_id)
        print("product id : ",product_id)
        
    except Product.DoesNotExist:
        return redirect('product_list')

    # Get or create the cart for the logged-in user
    cart, created = Cart.objects.get_or_create(user=request.user)  # Ensure user is the actual User instance

    # Get or create a CartProduct instance
    cart_product, created = CartProduct.objects.get_or_create(cart=cart, product=product)

    if created:
        # If product is not in cart, set quantity
        cart_product.quantity = quantity
        cart_product.save()
    else:
        # If product exists, increment quantity
        cart_product.quantity += quantity
        cart_product.save()

    # Redirect to the cart page
    return redirect('viewcart')

def remove_from_cart(request,product_id):
    cart = Cart.objects.get(user=request.user)
    cart_item = CartProduct.objects.get(cart=cart, product__id=product_id)
    cart_item.delete()

    return redirect('viewcart')



 