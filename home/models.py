from django.db import models
from django.contrib.auth.models import User


# class User(models.Model):
#     # user
#     first_name = models.CharField(max_length = 15, verbose_name = "first name")
#     last_name = models.CharField(max_length = 15, verbose_name = "last name")
#     username =  models.CharField(max_length = 15, verbose_name = "username", default = '')

#     age = models.IntegerField()

#     genders = [
#         ('M','Male'),
#         ('F','Female'),
#         ('O','Others'),
#     ]
#     gender = models.CharField(default = 'M',choices = genders, max_length = 1)
#     email = models.EmailField()

#     def __str__(self):
#         return f"{self.first_name} {self.last_name}" 

    
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
    
# class Cart(models.Model):
#     user = models.OneToOneField(User, on_delete = models.CASCADE)
#     product = models.ForeignKey(Product, on_delete = models.CASCADE, null = True)

#     def __str__(self):
#         return f"{self.user}'s Cart"       

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming you have a User model
    products = models.ManyToManyField(Product, through='CartProduct')  # Many-to-many relationship
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

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


    




