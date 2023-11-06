from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2)
    image_url = models.CharField(max_length=1000)
    category = models.CharField(max_length=100)
    open_for_bid = models.BooleanField(default=True)

class Bid(models.Model):
    bid = models.DecimalField(max_digits=8, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    listing_item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="item_for_bid")

class WatchListItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    listing_item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="item")

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    listing_item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="item_for")
    comment = models.CharField(max_length=1000)


