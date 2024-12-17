from django.db import models

class Product(models.Model):
    #as of now i am practicing so only keep the three values for the product
    name = models.CharField(max_length = 30, verbose_name = "product name")
    description = models.TextField(verbose_name = "product description")
    detail_description = models.TextField(default = '')
    price = models.IntegerField(verbose_name = "product price")
    image = models.ImageField(upload_to = 'product-images', default = 'default.jpg') 


    def __str__(self):
        return self.name
    
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