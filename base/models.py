from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class members(models.Model):
    user = models.ForeignKey(User , on_delete =models.SET_NULL,null=True , blank = True )

class Product(models.Model):
    name = models.CharField(max_length=100)
    brandname = models.CharField(max_length=100)
    mainprice = models.IntegerField()
    price = models.IntegerField()
    category = models.CharField(max_length=100)
    colour = models.CharField(max_length=20)
    discription = models.CharField(max_length=300)
    image = models.ImageField(upload_to='images/', null=True, blank=True)  # ImageField for product images
    arrival_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    