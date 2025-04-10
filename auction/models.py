from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist=models.ManyToManyField('Listing',blank=True,related_name="watchlisted_by")

class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Listing(models.Model):
    title=models.CharField(max_length=90)
    description=models.CharField(max_length=300)
    imageUrl=models.CharField(max_length=1000)
    isActive=models.BooleanField(default=True)
    owner=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="user")
    category = models.ForeignKey(Category, related_name="listing", on_delete=models.CASCADE, blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    starting_bid=models.DecimalField(max_digits=10,decimal_places=2)
    def __str__(self):
        return f"{self.title}"
    @property
    def current_price(self):
        highest=self.bids.order_by('-amount').first()
        return highest.amount if highest else self.starting_bid

class Bid(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    listing=models.ForeignKey('Listing',on_delete=models.CASCADE,related_name="bids")
    amount=models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return f"{self.user.username} bids Rs. {self.amount} on {self.listing}"

class Comment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    listing=models.ForeignKey('Listing',on_delete=models.CASCADE,related_name="comments")
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"comment by {self.user.username} on {self.listing}"
    

class Post(models.Model):
    owner = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    content = models.TextField(max_length=300)
    date = models.DateTimeField()