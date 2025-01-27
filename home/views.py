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
from rest_framework.views import APIView
from home.serializer import CategorySerializer, ProductSerializer, CartSerializer, LoginSerizlier, OrderSerializer, OrderItemsSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

class CategoryOperations(APIView):
    def get(self, request):
        query_set = Category.objects.all()
        print(query_set)
        serialized_data = CategorySerializer(query_set, many = True)
        
        return Response({"message":"Success","data":serialized_data.data})
    
class ProductByCategory(APIView):
    def get(self, request, cid):
        products = Product.objects.all().filter(category_id = cid)
        serialized_data = ProductSerializer(products, many = True)

        return Response({"message":"success","data":serialized_data.data})
    
class ProductDetail(APIView):
    def get(self, request, pid):
        try:
            product = Product.objects.get(id = pid)
            print(product)
            serialized_data = ProductSerializer(product)
            return Response({"message":"product details found","data":serialized_data.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message":"product details not found"},status=status.HTTP_404_NOT_FOUND)

class CartView(APIView):
    def get(self, request):
        cart,created = Cart.objects.get_or_create(user = request.user)  
        cart_products = CartProduct.objects.all().filter(cart = cart)
    
        # total = 0        
       
        for cart_product in cart_products:
            total += cart_product.product.price * cart_product.quantity
            net_amount = cart_product.product.price * cart_product.quantity
            cart_product.net_amount = net_amount
            cart_product.save()

        cart.total = total
        cart.save()

        serialized_data = CartSerializer(cart)
        return Response({"message":"cart details found","data":serialized_data.data},status = status.HTTP_200_OK)

class LoginAPI(APIView):
    def post(self,request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        deserialized_data = LoginSerizlier(data = request.data)
        if not deserialized_data.is_valid():
            return Response({"errors":deserialized_data.errors})
        
        user = authenticate(username = deserialized_data.data['email'], password = deserialized_data.data['password'])
        if user is not None:
            return Response(status=status.HTTP_302_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class ViewOrders(APIView):
    def get(self, reuqest, oid):
        orders_details = Orders.objects.all().get(id = oid)
        serialized_data = OrderSerializer(orders_details)

        return Response({"message":"order details found","data":serialized_data.data},status=status.HTTP_302_FOUND)
        # order_itmes = OrderItems.objects.all().filter(order__id = oid)

class ViewOrderDetails(APIView):
    def get(self, request, oid):
        try:
            order_itmes = OrderItems.objects.all().filter(order__id = oid)
            serialized_data = OrderItemsSerializer(order_itmes, many = True)
            return Response({"message":"orderdetails found","data":serialized_data.data},status=status.HTTP_302_FOUND)
        except Exception as e:
            return Response({"message":"no order details found"},status=status.HTTP_404_NOT_FOUND)

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

@login_required
def home_view(request):
    categories = Category.objects.all()
    return render(request,'home/home.html',{'categories':categories})

def view_products_by_category(request,cid):
    products = Product.objects.all().filter(category_id = cid)
    return render(request, 'home/products.html', {'products':products})

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
        email = request.POST.get('email')
        password = request.POST.get('password')

        # print(f"Username: {username}, Password: {password}")

        user = authenticate(username = email, password = password)

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
            if product.quantity < product.product.stock:
                
                product.quantity += 1
                product.save()

                product.net_amount = product.quantity * product.product.price 
                product.save()

                return redirect("viewcart")

            else:
                messages.warning(request,f"Sorry, only {product.product.stock} units are left in stock ☹️☹️☹️. You already have {product.product.stock} units in your cart.")
                return redirect('viewcart') 

        elif status == 'minus':
            if product.quantity == 1:
                remove_from_cart(request,product.product.id)
                return redirect('smart-phone')
            else:
                product.quantity -= 1
                product.save()
                product.net_amount = product.quantity * product.product.price 
                product.save()
                return redirect("viewcart")
        else:
            return redirect('viewcart')                 

def add_to_cart(request, product_id):
    quantity = 1
    
    if quantity <= 0:
        return redirect('product_list')

    product = Product.objects.get(id=product_id)

    cart, created = Cart.objects.get_or_create(user=request.user)  

    cart_product, created = CartProduct.objects.get_or_create(cart=cart, product=product)

    if created:
        cart_product.quantity = quantity
        cart_product.save()

    else:
        if cart_product.quantity < product.stock:
            cart_product.quantity += quantity
            cart_product.save()
        else:
            messages.warning(request,f"Sorry, only {product.stock} units are left in stock ☹️☹️☹️. You already have {product.stock} units in your cart.")
            return redirect('smart-phone') 



    messages.success(request,"Product added to cart 😃")        
    return redirect('smart-phone')

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
            messages.success(request, "Your order has been placed successfully 😍")
            users_cart.total = 0
            users_cart.save()

            return redirect('smart-phone')

    return render(request, 'home/checkout.html')    

def view_orders(request,oid):
    
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
            
            return render(request,'home/index.html',{"error":"Registered Successfully"})
    
    else:
        return render(request,'home/registration.html')
    

def custom_logout(request):
    logout(request)
    return redirect('login') 


 