from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Customer(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200,blank=False)
    address=models.CharField(max_length=200,blank=True)
    email=models.CharField(max_length=300,blank=False)

    def __str__(self):
        return self.name
    
def create(sender,instance,created,*args,**kwargs):
    if created:
        Customer.objects.create(user=instance,name=instance.username,email=instance.email)
        
post_save.connect(create,sender=User)

class Products(models.Model):
    category=(
        ('Beer','Beer'),
        ('whiskey','whiskey'),
         ('Wine','Wine'),
         ("Rum",'Rum'),
         ("Vodka","Vodka"),
        )
    name=models.CharField(max_length=200,blank=False)
    price= models.IntegerField(blank=False,)
    Description=models.CharField(max_length=400,blank=True)
    Category=models.CharField(choices=category,max_length=8)
    rating=models.IntegerField(default=0)
    quantity=models.IntegerField(default=0)
    image=models.ImageField(upload_to='images')
    date=models.DateTimeField(auto_now_add=True)
   
   
class Order(models.Model):
    customer=models.ForeignKey(Customer,null=True,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    status=models.BooleanField(default=False)
    transaction_id=models.CharField(max_length=200,null=True,blank=True)

    @property
    def get_total_products(self):
        items=self.cart_set.all()
        total=sum([item.quantity for item in items])
        return total
    
    @property
    def get_total_amount(self):
        items=self.cart_set.all()
        amount=sum([item.get_total_amount for item in items])
        return amount



class Cart(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE,null=True)
    order=models.ForeignKey(Order,null=True,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1,null=True,blank=False)
    
    def __str__(self) -> str:
        return self.product.name
    
    @property
    def get_total_amount(self):
        self.total=self.product.price* self.product.quantity
        return self.total



class Shipping(models.Model):
    customer=models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,blank=False,null=True)
    address=models.CharField(max_length=300,null=True,blank=False)
    phone=models.CharField(max_length=100,null=True,blank=False)
    email=models.CharField(max_length=300,null=True,blank=False)
    city=models.CharField(max_length=300,null=True,blank=False)
    state=models.CharField(max_length=300,null=True,blank=False)

    def __str__(self):
        return self.address