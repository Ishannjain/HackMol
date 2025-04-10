from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator


from .models import *

import datetime

def index(request):
    
    return render(request,"auction/index.html",{
        "all_categories":Category.objects.all()
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
            return render(request, "auction/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auction/login.html")


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
            return render(request, "auction/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auction/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auction/register.html")
    

def create_listing(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if request.method == "POST":
        title=request.POST.get("title")
        description=request.POST.get("description")
        starting_bid=request.POST.get("starting_bid")
        imageUrl=request.POST.get("imageUrl")


        cat_id=request.POST.get("category")
        category = Category.objects.filter(pk = cat_id).first()

        listing=Listing(
            title=title,
            description=description,
            starting_bid=starting_bid,
            imageUrl=imageUrl,
            category=category,
            owner=request.user
        )
        listing.save()
        return HttpResponseRedirect(reverse(index))
    
    return render(request,"auction/create.html", {
        "categories": Category.objects.all()
    })

def listing(request,listing_id):
    listing=get_object_or_404(Listing,pk=listing_id)
    user = request.user
    in_watchlist=user.is_authenticated and listing in user.watchlist.all()
    highest_bid=listing.bids.order_by("-amount").first()
    is_creator=listing.owner == user
    winner=highest_bid.user if highest_bid else None
    is_winner=winner==user
    comments=listing.comments.all().order_by("-created_at")

    message=None
    message_type=None
    #handling post requests for bid,watchlist_toggle,close auction,comment
    if request.method=='POST':
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))
        if 'place_bid' in request.POST:
            bid_amount=request.POST.get("bid")
            bid_amount=float(bid_amount)
            current_price=listing.current_price
            try:
                if bid_amount<=current_price:
                    message="Amount of the bid must be higher then current Price "
                    message_type="error"
                    # messages.error(request,"Amount of the bid must be higher then current Price ")
                    # return HttpResponseRedirect(reverse("listing",args=[listing.id]))
                else:
                    bid=Bid(user=user,listing=listing,amount=bid_amount)
                    bid.save()
                    message="Bid saved successfully"
                    message_type="success"
                    # messages.success(request,"Bid saved successfully")
                    # return HttpResponseRedirect(reverse("listing",args=[listing.id]))
            except:
                message="Invalid Bid"
                message_type="error"
                # return HttpResponseRedirect(reverse("listing",args=[listing.id]))
        elif 'watchlist_toggle' in request.POST:
            if in_watchlist:
                user.watchlist.remove(listing)
                message="Item removed from the watchList"
                message_type="info"
            else:
                user.watchlist.add(listing)
                message="Item added to the watchlist"
                message_type="success"
            in_watchlist=not in_watchlist
            # return HttpResponseRedirect(reverse("listing",args=[listing.id]))
        elif 'close_auction' in request.POST:
            listing.is_active=False
            listing.save()
            message="Auction closed Successfully"
            message_type="success"
            # return HttpResponseRedirect(reverse("listing",args=[listing.id]))
        elif 'comment_submit' in request.POST:
            content=request.POST.get("comment")
            if content:
                comment=Comment(user=user,listing=listing,content=content)
                comment.save()
                message="Comment saved Successfully"
                message_type="success"
            # return HttpResponseRedirect(reverse("listing",args=[listing.id]))



    return render(request,"auction/listing.html",{
        "listing":listing,
        "in_watchlist":in_watchlist,
        "highest_bid":highest_bid,
        "is_creator":is_creator,
        "winner":winner if not listing.isActive else None,
        "is_winner":is_winner,
        "comments":comments,
        "message":message,
        "message_type":message_type
    })


def watchlist(request,user_id):
    all_listings=request.user.watchlist.all()
    return render(request,"auction/watchlist.html",{
        "all_listings":all_listings
    })


def category(request,category_name):
    active_listings = Listing.objects.filter(isActive=True)
    listing_of_this_category=[]
    for listing in active_listings:
        if listing.category==category_name:
            listing_of_this_category.append(listing)

    category = Category.objects.filter(title = category_name).first()
    listings = Listing.objects.filter(category = category)

    return render(request,"auction/category.html",{
        "listings":listings,
        "category":category_name
    })


def user_listing(request, user_id):
    user = User.objects.get(pk = user_id)
    print(user)
    listings = Listing.objects.filter(owner = user)
    
    return render(request,"auction/category.html",{
        "listings":listings,
        "category":f"{user}'s Listings"
    })





def posts(request):
    allPosts = Post.objects.all().order_by("date").reverse()
    paginator = Paginator(allPosts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    
    return render(request, "auction/posts.html", {
        "posts": allPosts,
        "user": request.user,
        "page_obj": page
    })


def newPost(request):
    if request.method == "POST":
        content = request.POST["content"]
        current_time = datetime.datetime.now().replace(microsecond=0)
        post = Post (
            content = content,
            owner = request.user,
            date = current_time
        )
        post.save()
        return HttpResponseRedirect(reverse("posts"))
