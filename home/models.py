from django.db import models
from django.contrib.auth.models import User
    
class Category(models.Model):
    name = models.CharField(max_length = 30, verbose_name = "category name", default = 'blank') 
    description = models.TextField(default = 'blank')
    photo = models.ImageField(upload_to = 'categoyr-images', default = 'default.jpg')

    def __str__(self):
        return self.name   

class Product(models.Model):
    #as of now i am practicing so only keep the three values for the product
    category = models.ForeignKey(Category, on_delete = models.CASCADE, default = 1)
    name = models.CharField(max_length = 30, verbose_name = "product name")
    description = models.TextField(verbose_name = "product description")
    detail_description = models.TextField(default = '')
    price = models.IntegerField(verbose_name = "product price")
    stock = models.IntegerField(verbose_name = "available stock", default = 0)
    image = models.ImageField(upload_to = 'product-images', default = 'default.jpg') 
    
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming you have a User model
    total = models.IntegerField(default = 0)

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    net_amount = models.IntegerField(default = 0)

    def __str__(self):
        return f"{self.product.name} in {self.cart.user.username}'s cart"


class Reviews(models.Model):
    #created this model to store the reviews of each product
    phone = models.ForeignKey(Product, on_delete = models.CASCADE)
    name = models.CharField(max_length = 30,verbose_name = "reviewers name") 
    review = models.TextField() 
    ratings = [
        (1,'bad'),
        (2,'avg'),
        (3,'good'),
        (4,'very good'),
        (5,'excellent')]   
    rating = models.IntegerField(choices = ratings,default = 3,verbose_name = "product rating")

class Orders(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    order_total = models.IntegerField()
    country = models.CharField(max_length = 30)
    city = models.CharField(max_length = 30)
    district = models.CharField(max_length = 30)
    address = models.TextField()
    order_date = models.DateTimeField(auto_now_add = True)
    delivery_date = models.DateField()

    def __str__(self):
        return f"{self.user.username}'s order"
    

class OrderItems(models.Model):
    order = models.ForeignKey(Orders, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.IntegerField()  
    net_amount = models.IntegerField(default = 0)

    def __str__(self):
        return f"order id = {self.order.id} items"

        





    




