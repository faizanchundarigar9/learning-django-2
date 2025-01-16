from django.urls import path
from django.shortcuts import render, redirect
from .models import Product, Reviews, Category
from django.shortcuts import get_object_or_404
from .forms import  CheckoutForm
from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import HttpResponse
from .models import Orders, OrderItems
from django.contrib import messages
from .models import Cart, CartProduct 
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from datetime import datetime
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


@login_required
def home_view(request):
    categories = Category.objects.all()
    return render(request,'home/home.html',{'categories':categories})

def view_products_by_category(request,cid):
    products = Product.objects.all().filter(category_id = cid)
    return render(request, 'home/products.html', {'products':products})

def reviews(request,pid):
    
    product = Product.objects.get(id = pid)
    reviews = Reviews.objects.filter(phone=product)
    return render(request, 'home/reviews.html',{'reveiws':reviews})

def details(request,pid):

    product = Product.objects.get(id = pid)
    return render(request, 'home/product_details.html',{'product':product})

def search_result(request):
    
    searchterm = request.GET.get('searchterm', '')
    products = Product.objects.filter(name__contains = searchterm)
    return render(request, 'home/products.html',{'products' : products})

def login_view(request):

    if request.method == 'POST':
        # print("post request received")
        username = request.POST.get('username')
        password = request.POST.get('password')

        # print(f"Username: {username}, Password: {password}")

        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('smart-phone')
        
        else:
            return render(request,'home/index.html', {'error': 'Invalid credentials.'})

    else:
        return render(request, 'home/index.html')  

def cart_view(request):
    
    cart,created = Cart.objects.get_or_create(user = request.user)  
    cart_products = CartProduct.objects.all().filter(cart = cart)

    total = 0        
    for cart_product in cart_products:
        total += cart_product.product.price * cart_product.quantity
        net_amount = cart_product.product.price * cart_product.quantity
        cart_product.net_amount = net_amount
        cart_product.save()

        cart.total = total
        cart.save()

    context = {
        'cart': cart,
        'cart_products': cart_products,
    }

    return render(request, 'home/cart.html', context)

def quantity_counter(request,cpid):

    if request.method == "GET":
        status = request.GET.get('status')
        
        product = CartProduct.objects.get(id = cpid) 

        if status == 'plus':
            
            if product.product.stock == 0:
                messages.warning(request,"out of stock")

            if product.product.stock != 0:
                product.quantity += 1
                product.save()

                # product.product.stock -= 1
                # product.product.save()

                product.net_amount = product.quantity * product.product.price 
                product.save()

                return redirect('viewcart')
            else:
                return redirect('viewcart')
        
        elif status == 'minus':
            if product.quantity != 1:
                product.quantity -= 1
                product.save()

                # product.product.stock += 1
                # product.product.save()

                product.net_amount = product.quantity * product.product.price 
                product.save()

            return redirect('viewcart')
    else:
        return redirect('viewcart')    

def add_to_cart(request, product_id):
    quantity = 1
    
    if quantity <= 0:
        return redirect('product_list')

    try:
        product = Product.objects.get(id=product_id)
        
    except Product.DoesNotExist:
        return redirect('product_list')

    cart, created = Cart.objects.get_or_create(user=request.user)  

    cart_product, created = CartProduct.objects.get_or_create(cart=cart, product=product)

    if created:
        cart_product.quantity = quantity
        cart_product.save()

        # cart_product.product.stock -= 1
        # cart_product.product.save() 
    else:
        cart_product.quantity += quantity
        cart_product.save()

        # cart_product.product.stock -= 1
        # cart_product.product.save() 

    return redirect('viewcart')

def remove_from_cart(request,product_id):
    cart = Cart.objects.get(user=request.user)
    cart_item = CartProduct.objects.get(cart=cart, product__id=product_id)
    cart_item.delete()

    cart.total = 0
    cart.save()

    return redirect('viewcart')


def checkout(request):

    if request.method == 'POST':
        form = CheckoutForm(request.POST)

        if form.is_valid():
            
            #getting users then after its cart
            user = request.user
            users_cart = Cart.objects.get(user = user)

            #getting items there in the cart
            cart_products = CartProduct.objects.all().filter(cart = users_cart)

            data = form.cleaned_data
            order = Orders(city = data['city'], country = data['country'], district = data['district'], user = user, delivery_date = '2025-04-04', order_total = users_cart.total, address = data['address'])
            order.save()

            #inserting products into the order items
            for cart_product in cart_products:
                cart_product.product.stock -= cart_product.quantity
                cart_product.product.save()
                OrderItems.objects.create(order = order ,product = cart_product.product, quantity = cart_product.quantity, net_amount = cart_product.net_amount)

            cart_products.delete()
            messages.success(request, "Your order has been placed successfully")
            users_cart.total = 0
            users_cart.save()

            return redirect('smart-phone')

    return render(request, 'home/checkout.html')    

def view_orders(request,oid):
    #getting the user instance
    user = request.user

    
    orders_details = Orders.objects.all().get(id = oid)
    
    order_itmes = OrderItems.objects.all().filter(order__id = oid)

    context = {'orders':order_itmes,'order_details':orders_details}

    return render(request,'home/orderhistory.html',context) 

def number_of_orders(request):

    user = request.user
    number_of_orders = Orders.objects.all().filter(user = user).count()
    orders = Orders.objects.all().filter(user = user).order_by('-id')

    return render(request,'home/orders.html',{'number_of_orders':number_of_orders,'orders':orders})

def category_search(request):
    if request.method == 'GET':
        categories = Category.objects.all().filter(name__contains = request.GET.get('searchterm'))
        return render(request,'home/home.html',{'categories':categories})

def view_profile(request):
    user_details, created = Profile.objects.get_or_create(user = request.user)
    return render(request,'home/profile.html',{'user_details':user_details})

def create_account(request):
    if request.method == 'POST':
        username = request.POST.get('first_name') + request.POST.get('last_name')
        if User.objects.all().filter(username = username).exists():
            messages.warning(request,"User already exists with this username")
            return redirect('create_account')
        
        if User.objects.all().filter(email = request.POST.get('email')).exists() and Profile.objects.all().filter(contact_number = request.POST.get('phone')).exists():
            messages.warning(request,"User already exists with this mobile number and email")
            return redirect('create_account')
        
        if User.objects.all().filter(email = request.POST.get('email')).exists():
            messages.warning(request,"User already exists with this email")
            return redirect('create_account')
        
        if Profile.objects.all().filter(contact_number = request.POST.get('phone')).exists():
            messages.warning(request,"Mobile number is already used and having account")
            return redirect('create_account')
        else:

            birth_date = datetime.strptime(request.POST.get('birthday'), '%d/%m/%Y').strftime('%Y-%m-%d')

            user = User.objects.create(username = request.POST.get('first_name') + request.POST.get('last_name'),first_name = request.POST.get('first_name'),last_name = request.POST.get('last_name'), email = request.POST.get('email'), password = make_password(request.POST.get('password')))

            user_profile = Profile.objects.create(user = user, birth_date = birth_date,contact_number = request.POST.get('phone'))
            return render(request,'home/index.html',{"error":f"your username will be : {username}",'status':True})
    
    else:
        return render(request,'home/registration.html')
    

def custom_logout(request):
    logout(request)
    return redirect('login') 


 