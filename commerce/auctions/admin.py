from django.contrib import admin
from .models import*

admin.site.register(Bid)
admin.site.register(AuctionListing)
admin.site.register(WatchListItem)
admin.site.register(Comment)