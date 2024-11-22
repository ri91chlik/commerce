from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comment, Bid

def removeWatchList(request, id):
    listingsInfo = Listing.objects.get(pk= id)
    currentClient= request.user
    listingsInfo. watchlist.remove(currentClient)
    return HttpResponseRedirect(reverse("listing", args=(id, )))
    

def addWatchList(request, id):
    listingsInfo = Listing.objects.get(pk= id)
    currentClient= request.user
    listingsInfo.watchlist.add(currentClient)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def comment1(request, id):
    currentClient= request.user
    listingsInfo = Listing.objects.get(pk= id)
    message= request.POST['new_comment']

    new_comment= Comment(
        author= currentClient,
        listing= listingsInfo,
        message= message,
    )
    new_comment.save()
    return HttpResponseRedirect(reverse("listing", args=(id, )))


def AnnexBid(request, id):
    newBid= request.POST.get('newBid')
    listingsInfo = Listing.objects.get(pk= id)
    IsListingInWatchList= request.user in listingsInfo.watchlist.all()
    allComments= Comment.objects.filter(listing= listingsInfo)
    IsListingInWatchList= request.user in listingsInfo.watchlist.all()
    if  int(newBid) > listingsInfo.price.bid:
        updateBid = Bid(user= request.user, bid= int(newBid))
        updateBid.save()
        listingsInfo.price = updateBid
        listingsInfo.save()
        isOwner = request.user.username ==listingsInfo.Owner.username
        return render(request, "auctions/listing.html",{ 
            "listing":listingsInfo,
            "message": "AnnexBid updated",
            "update" : True,
            "IsListingInWatchList":IsListingInWatchList,
            "allComments": allComments,
            "isOwner": isOwner,
    })
    else:
        return render(request, "auctions/listing.html",{ 
            "listing":listingsInfo,
            "message": "Bid unsuccessful",
            "update" : False,
            "IsListingInWatchList":IsListingInWatchList,
            "allComments": allComments,
            
            
    })


    


def show_watchlist(request):
    currentClient= request.user
    listings= currentClient.uswatchlist.all()
    return render(request, "auctions/watchlist.html", {
        "Listings": listings
    
    })

def listing(request, id):
    listingsInfo = Listing.objects.get(pk= id)
    IsListingInWatchList= request.user in listingsInfo.watchlist.all()
    allComments= Comment.objects.filter(listing= listingsInfo)
    isOwner = request.user.username ==listingsInfo.Owner.username
    return render(request, "auctions/listing.html",{ 
        "listing": listingsInfo,
        "IsListingInWatchList":IsListingInWatchList,
        "allComments": allComments,
        "isOwner": isOwner,
    })

def terminateAuction(request, id):
    listingsInfo = Listing.objects.get(pk= id)
    listingsInfo.isActive = False
    listingsInfo.save()
    isOwner = request.user.username == listingsInfo.Owner.username
    IsListingInWatchList= request.user in listingsInfo.watchlist.all()
    allComments= Comment.objects.filter(listing= listingsInfo)
    return render(request, "auctions/listing.html",{
        "listing": listingsInfo,
        "IsListingInWatchList":IsListingInWatchList,
        "allComments": allComments,
        "isOwner": isOwner,
        "update" : True,
        "message":"Bravo, you are the winner",
    })



def index(request):
    active_Listings = Listing.objects.filter(isActive= True)
    allCat = Category.objects.all()
    return render(request, "auctions/index.html",{ 
        "Listings":active_Listings,
        "categories": allCat,
    })

def show_category(request):
    if  request.method == "POST":
        form_category= request.POST['category']
        category= Category.objects.get(categoryName=form_category)
        active_Listings = Listing.objects.filter(isActive= True, category= category)
        allCat = Category.objects.all()
        return render(request, "auctions/index.html",{ 
            "Listings":active_Listings,
            "categories": allCat,
    })

def create_listing(request):
    if request.method == "GET":
        allCat = Category.objects.all()
        return render(request, "auctions/create.html", {
                      "categories":allCat
    })
    else:
        # obtain data from the form
        title= request.POST.get("title")
        imageUrl= request.POST.get("imageUrl")
        description= request.POST.get("description")
        price= request.POST.get("price")
        category= request.POST.get("category")
        # user
        currentClient= request.user
        #category content
        categoryInfo = Category.objects.get(categoryName= category)
        #bid
        bid= Bid(bid=int(price), user= currentClient)
        bid.save()
        #new listing object
        N_Listing= Listing(
            title= title,
            description= description,
            imageUrl= imageUrl,
            price= bid,
            category= categoryInfo,
            Owner=currentClient
        )
        #save the object in the database
        N_Listing.save()
        #redirect to index page
        return HttpResponseRedirect(reverse("index"))

    


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
