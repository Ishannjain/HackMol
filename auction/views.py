from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
import json
from django.http import JsonResponse, HttpResponseForbidden


from .models import *

import datetime
import random, string


def check(password):
    if len(password) < 8:
        return False
    isUpper = False
    isLower = False
    isDigit = False
    for ch in password:
        if ch.isupper():
            isUpper = True
        if ch.islower():
            isLower = True
        if ch.isdigit():
            isDigit = True
    
    return isUpper and isLower and isDigit

def generate_unique_code():
    from .models import Listing
    while True:
        code = ''.join(random.choices(string.digits, k=6))
        if not Listing.objects.filter(room_id=code).exists():
            return code


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
        
        if not check(password):
                    return render(request, "auction/register.html", {
                        "message": "Passwords does not meet requirements. Minimun length 8 and should contain atleast one Capital Letter, one small Letter and one digit"
                    })

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
        mode = request.POST.get('mode')


        cat_id=request.POST.get("category")
        category = Category.objects.filter(title = cat_id).first()

        if mode == "private" :
            listing=Listing(
                title=title,
                description=description,
                starting_bid=starting_bid,
                imageUrl=imageUrl,
                category=category,
                owner=request.user,
                isPrivate = True,
                room_id = generate_unique_code(),
                password = request.POST.get('password')
            )
            listing.save()
            return HttpResponseRedirect(reverse(index))

        else :
            listing=Listing(
                title=title,
                description=description,
                starting_bid=starting_bid,
                imageUrl=imageUrl,
                category=category,
                owner=request.user,
                isPrivate = False
            )
            listing.save()
            return HttpResponseRedirect(reverse(index))

        

    
    return render(request,"auction/create.html", {
        "categories": Category.objects.all()
    })

def findListing(request):
    if request.method == "POST":
        room = request.POST.get("room_id")
        password = request.POST.get("password")
        listing = Listing.objects.filter(isPrivate = True, room_id = room, password = password).first()
        if listing:
            user = request.user
            in_watchlist=user.is_authenticated and listing in user.watchlist.all()
            highest_bid=listing.bids.order_by("-amount").first()
            is_creator=listing.owner == user
            winner=highest_bid.user if highest_bid else None
            is_winner=winner==user
            comments=listing.comments.all().order_by("-created_at")
            return render(request,"auction/listing.html",{
            "listing":listing,
            "in_watchlist":in_watchlist,
            "highest_bid":highest_bid,
            "is_creator":is_creator,
            "winner":winner if not listing.isActive else None,
            "is_winner":is_winner,
            "comments":comments
            })
        else:
            return render(request, "auction/findRoom.html", {
                "message": "Id or password is incorrect"
            })
    return render(request, "auction/findRoom.html")


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
            listing.isActive=False
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
    listings = Listing.objects.filter(category = category, isPrivate = False)

    return render(request,"auction/category.html",{
        "listings":listings,
        "category":category_name
    })


def user_listing(request, user_id):
    user = User.objects.get(pk = user_id)
    print(user)
    if user == request.user:
        listings = Listing.objects.filter(owner = user)
    else:
        listings = Listing.objects.filter(owner = user, isPrivate = False)
    
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


def edit(request, post_id):
    if request.method == "POST":
        post = Post.objects.get(pk = post_id)
        body = json.loads(request.body)
        post.content = body["content"]
        post.save()
        return JsonResponse({"message": "Change successful", "data": body["content"]})    

def following(request):
    currUser = request.user

    followed_users = Follow.objects.filter(follower=currUser).values_list('followed', flat=True)

    posts = Post.objects.filter(owner__in=followed_users).order_by('date')

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, "auction/following.html", {
        "posts": posts,
        "user": currUser,
        "page_obj": page
    })

def profile(request, user_id):
    if request.method == "POST":
        rating = request.POST.get("rating")
        try:
            rating = float(rating)
            if not (1 <= rating <= 5):
                return HttpResponse("Invalid rating. Must be between 1 and 5.")
        except (ValueError, TypeError):
            return HttpResponse("Invalid rating format.")

        user = User.objects.get(pk=user_id)
        curr_user = request.user

        # Prevent double rating
        if curr_user in user.noOfRatings.all():
            return HttpResponse("You've already rated this user.")

        temp = float(user.rating) * len(user.noOfRatings.all()) + rating
        user.noOfRatings.add(curr_user)
        user.rating = temp / (len(user.noOfRatings.all()))
        user.save()

        return HttpResponseRedirect(reverse("profile", args=(user.id,)))

    currUser = request.user
    user = User.objects.get(pk=user_id)
    followings = Follow.objects.filter(follower = user).values_list('followed', flat=True)
    followers = Follow.objects.filter(followed = user).values_list('follower', flat=True)
    posts = Post.objects.filter(owner = user).order_by('date').reverse()

    follows = currUser.id in followers

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, "auction/profile.html", {
        "loadedUser": user,
        "user": currUser,
        "following": followings,
        "follower": followers,
        "posts": posts,
        "follows": follows,
        "page_obj": page
    })


def follow(request, user_id):
    currUser = request.user
    user = User.objects.get(pk = user_id)
    follow = Follow(
        follower = currUser,
        followed = user 
    )
    follow.save()
    return HttpResponseRedirect(reverse("profile", args=(user.id,)))


def unfollow(request, user_id):
    currUser = request.user
    user = User.objects.get(pk = user_id)
    print(user, currUser)
    follow = Follow.objects.filter(follower = currUser, followed = user)
   
    follow.delete()
    return HttpResponseRedirect(reverse("profile", args=(user.id,)))



def like(request, post_id):
    post = Post.objects.get(pk = post_id)
    post.likes.add(request.user)
    return JsonResponse({"message": "Like added!"})

def unlike(request, post_id):
    post = Post.objects.get(pk = post_id)
    post.likes.remove(request.user)
    return JsonResponse({"message": "Like removed!"})


def delete_post(request, post_id):
    if request.method == "DELETE":
        try:
            post = Post.objects.get(pk=post_id)
            if post.owner != request.user:
                return HttpResponseForbidden("You cannot delete someone else's post.")
            post.delete()
            return JsonResponse({"message": "Post deleted successfully."})
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)
    return JsonResponse({"error": "Invalid request method."}, status=400)