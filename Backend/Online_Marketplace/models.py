from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

#Using User Extension for user table
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    isSeller = models.BooleanField(default=False)
    cardNum = models.UUIDField(default=uuid.uuid4, editable=False)
    profileImgLink = models.CharField(max_length=500, blank=True, default="")

    def __str__(self):
        #get the profile as username
        return self.user.username
    
#Cart table
class Cart(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart of {self.user.username}"
    
#Product Table
class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    productimg = models.ImageField(upload_to='product_images/', blank=True, null=True)

    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
#Cart items table
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.IntegerField()

#Order Table
class Order(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    orderDate = models.DateTimeField(auto_now_add=True)
    billing = models.CharField(max_length=150)

#Order items Table
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.IntegerField()
    priceAtPurchase = models.DecimalField(max_digits=6, decimal_places=2)

