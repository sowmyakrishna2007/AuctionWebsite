from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms

from .models import*

CATEGORIES = [
    ('furniture', 'Furniture'),
    ('clothing', 'Clothing'),
    ('entertainment', 'Entertainment'),
    ('sports', 'Sports'),
    ('technology', "Technology")
    ]

class NewListing(forms.Form): 
    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control col-md-8 col-lg-8'}))
    description = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'class':'form-control col-md-8 col-lg-8'}))
    starting_bid = forms.DecimalField(widget=forms.TextInput(attrs={'class':'form-control col-md-8 col-lg-8'}))
    image_url = forms.CharField(max_length=1000, widget=forms.TextInput(attrs={'class':'form-control col-md-8 col-lg-8'}))
    category = forms.CharField(widget=forms.Select(choices=CATEGORIES, attrs={'class':'form-control col-md-8 col-lg-8'}))


def index(request):
    return render(request, "auctions/index.html", {
        "listings": AuctionListing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def add_listing(request):
    if request.method == "GET":
        return render(request, "auctions/add_listing.html", {
            "form": NewListing
        })
    else:
        form = NewListing(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = request.user
            title = data["title"]
            description = data["description"]
            starting_bid = float(data["starting_bid"])
            image_url = data["image_url"]
            category = data["category"]
            listing = AuctionListing(user=user, title=title, description=description, starting_bid=starting_bid, image_url=image_url, category=category)
            listing.save()
            return redirect(index)

def find_bid(listing_item):
    bids_for_item = Bid.objects.all().filter(listing_item=listing_item)
    current_max = -1
    current_bid = None
    for i in bids_for_item:
        if i.bid > current_max:
            current_max = i.bid
            current_bid = i

    return current_bid

def bid(request, id):
    auction_list = AuctionListing.objects.all().get(pk=int(id))
    x = False
    for i in WatchListItem.objects.all():
            if i.listing_item == auction_list and i.user == request.user:
                x = True
    item = request.POST["bid_value"]
    print(item)
    new_bid = Bid(user=request.user, bid=float(item), listing_item=auction_list)
    new_bid.save()

    return redirect(listing, id=id)

def close_bid(request, id):
    auction_list = AuctionListing.objects.all().get(pk=int(id))
    auction_list.open_for_bid = not auction_list.open_for_bid
    auction_list.save()

    return redirect(listing, id=id)

def watch(request, id):
    auction_list = AuctionListing.objects.all().get(pk=int(id))
    x = False
    for i in WatchListItem.objects.all():
        if i.listing_item == auction_list and i.user == request.user:
                x = True
    if not x:
        item = WatchListItem(user=request.user, listing_item=auction_list)
        item.save()
    else:
        item = WatchListItem.objects.all().get(listing_item=auction_list, user=request.user)
        item.delete()
    
    return redirect(listing, id=id)


def listing(request, id):
    auction_list = AuctionListing.objects.all().get(pk=int(id))
    current_bid = find_bid(auction_list)
    if request.method == "GET":
        x = False
        for i in WatchListItem.objects.all():
            if i.listing_item == auction_list and i.user == request.user:
                x = True

        return render(request, "auctions/listing.html", {
            "listing": auction_list,
            "watching": x,
            "bid": current_bid,
            "comments":Comment.objects.all().filter(listing_item=auction_list)
        })

def watchlist(request):
    user = request.user
    all_watchlist_items = WatchListItem.objects.all().filter(user=user)
    return render(request, "auctions/watchlist.html", {
        "items":all_watchlist_items
    })

def comments(request, id):
    if request.method == "POST":
        comment = Comment(user=request.user, comment=request.POST["comment"], listing_item = AuctionListing.objects.all().get(pk=int(id)))
        comment.save()
        return redirect(listing, id=id)

def category_page(request):
    print([i[1] for i in CATEGORIES])
    return render(request, "auctions/categories.html", {
        "categories": [i[1] for i in CATEGORIES]
    })

def category(request, category):
    return render(request, "auctions/category.html", {
        "listings": AuctionListing.objects.all().filter(category=category.lower()),
        "category": category
    })           

