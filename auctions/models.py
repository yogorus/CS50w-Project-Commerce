from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', blank=True, related_name='watchlist')


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='listings', blank=True, null=True, default='No Category')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.id}: {self.title} by {self.author}"


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment on {self.listing.id}: {self.listing.title} by {self.author}'


class Bid(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Bid on {self.listing.title} for {self.amount}$ by {self.author}'