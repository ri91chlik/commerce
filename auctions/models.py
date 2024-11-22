from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
class Category(models.Model):
    categoryName = models.CharField(max_length=60)

    def __str__(self):
        return self.categoryName
    
class Bid(models.Model):
    bid= models.IntegerField()
    user= models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userBid")

class Listing(models.Model):
    title = models.CharField(max_length=35)
    description= models.CharField(max_length=320)
    imageUrl= models.CharField(max_length=950)
    price= models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="priBid")
    isActive=models.BooleanField(default=True)
    Owner=models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    category= models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    watchlist= models.ManyToManyField(User, blank=True,null= True, related_name="uswatchlist")
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    author= models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user2")
    listing= models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listing")
    message= models.CharField(max_length=320)
    def __str__(self):
        return f"{self.author} comment on {self.listing}"
