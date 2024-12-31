from django.contrib import admin
from .models import Product, Reviews, Category, Orders, OrderItems, Cart, CartProduct

admin.site.register(Reviews)


class CustomOrders(admin.ModelAdmin):
    list_display = ('id','user', 'order_total', 'country', 'city', 'district', 'address', 'order_date', 'delivery_date')

class CustomOrderItems(admin.ModelAdmin):
    list_display = ('id','order','product','quantity')

class CustomProducts(admin.ModelAdmin):
    list_display = ('id','category','name','description','detail_description','price','stock')

class CustomCategory(admin.ModelAdmin):
    list_display = ('id','name','description')    

admin.site.register(Category, CustomCategory)
admin.site.register(Product,CustomProducts)
admin.site.register(Orders,CustomOrders)
admin.site.register(OrderItems,CustomOrderItems)
admin.site.register(Cart)
admin.site.register(CartProduct)

