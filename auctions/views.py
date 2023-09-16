from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *
from .utils import *


def all(request):
    # Load & render all auctions
    return render(request, "Auctions/index.html", {
        "auctions": Auction.objects.all().order_by("-id"),
        "empty_message": "There are no listings.",
        "type": "All Listings",
    })

    
def index(request):
    # Load & render active auctions
    return render(request, "auctions/index.html", {
        "auctions": Auction.objects.filter(is_active=True).order_by("-id"),
        "empty_message": "There are no currently active listings.",
        "type": "Active Listings",
    })

@login_required(login_url="/login/")
def watchlist(request):
    # Load & render all auctions that have been added to the user's watchlist.
    return render(request, "auctions/index.html", {
        "auctions": Auction.objects.filter(watchlist_auction__user=request.user),
        "empty_message": "You haven't added any listings to your watchlist.",
        "type": "Watchlist",
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
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url="/login/")
def new(request):
    form = None
    if request.method == "POST":
        form = AuctionForm(request.POST)
        if form.is_valid():
            auction = form.save(commit=False)
            auction.created_by = request.user
            auction.save()
            return HttpResponseRedirect(reverse("auctions:index"))
        
    if not form:
        form = AuctionForm()
    
    return render(request, "auctions/new.html", {
        "form": form
    })


def no_listing(request):  # in case id was not provided:
    return HttpResponseRedirect(reverse("auctions:index"))

def listing(request, id, err_list=None, success_msg=None, watchlist=None):
    comment_form, bid_form = None, None
    auction = Auction.objects.get(id=id)
    
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if not success_msg:
            bid_form = BidForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.auction = auction
            comment.commenter = request.user
            comment.save()
            return HttpResponseRedirect(reverse("auctions:listing", args=[id]))

    if not bid_form:
        bid_form = BidForm()
        
    print(success_msg)
    return render(request, "auctions/listing.html", {
        "auction": Auction.objects.get(id=id),
        "is_in_watchlist": is_in_watchlist(request, auction=auction),
        "comments": Comment.objects.filter(auction=auction).order_by("-date"),
        "comment_form": CommentForm(),
        "bid_form": bid_form,
        "err_list": err_list,
        "success_msg": success_msg,
        "watchlist": watchlist

    })


@login_required(login_url="/login/")
def bid(request, id):
    form = None
    if request.method == "POST":
        form = BidForm(request.POST, initial={"auction_id": id})
        if form.is_valid():
            bid = form.save(commit=False)
            auction = Auction.objects.get(id=id)
            bid.auction_id = auction
            bid.bidder = request.user
            auction.current_bid = bid
            bid.save()
            auction.save()
            success_msg ="Your bid was successfully registered in the system."
            return listing(request, id, success_msg=success_msg)

    if not form:
        form = BidForm()
    else:
        err_list = []
        for field in form:
            if field.errors:
                for error in field.errors:
                    err_list.append(str(error))
    return listing(request, id, err_list=err_list)

@login_required(login_url="/login/")
def is_in_watchlist(request , auction):
    data = Watchlist.objects.filter(user=request.user, auction=auction).exists()    
    return data



@login_required(login_url="/login/")
def watchlist_add(request, id):
    auction = Auction.objects.get(id=id)
    if not is_in_watchlist(request, auction):
        watchlist = Watchlist(user=request.user, auction=auction)
        watchlist.save()
    return listing(request, id, watchlist=True)
    # return HttpResponseRedirect(reverse("auctions:listing", args=[id]))


@login_required(login_url="/login/")
def watchlist_remove(request, id):
    auction = Auction.objects.get(id=id)
    if is_in_watchlist(request, auction):
        watchlist = Watchlist.objects.filter(
            user=request.user, auction=auction)
        watchlist.delete()
    return listing(request, id, watchlist=False)

@login_required(login_url="/login/")
def edit(request, id):
    if request.method == "POST":
        pass
    
    return render(request, "auctions/edit.html", {
        "form": AuctionForm
    })
    

@login_required(login_url="/login/")
def close(request, id):
    if auction := Auction.objects.get(id=id):
        if request.user == auction.created_by and auction.is_active:
            if auction.current_bid is not None:
                auction.winner = auction.current_bid.bidder
            auction.end_time = timezone.now()
            auction.is_active = False
            auction.save()
            
    return HttpResponseRedirect(reverse("auctions:listing", args=[id]))
    
def categories(request):
    auctions = Auction.objects.filter(is_active=True).order_by("-id")
    categories = sort_categories(auctions)
    return render(request, "auctions/categories.html", {
        "categories": categories,
    })
        
    