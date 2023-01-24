from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db.models import Max


from .models import User, Listing, Category, Comment, Bid
from .forms import ListingForm, CommentForm, BidForm, CHOICES


def index(request):
    listings = Listing.objects.all().order_by('-date')
    return render(request, "auctions/index.html", {
        "listings" : listings,
        "header": 'Active Listings'
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


@login_required
def create(request):
    if request.method == "POST":
        
        form = ListingForm(request.POST)

        if form.is_valid():

            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            image = form.cleaned_data['image']
            try:
                category = Category.objects.get(name=form.cleaned_data['category'])
            except Category.DoesNotExist:
                category = None
            author = request.user

            listing = Listing(title=title, description=description, price=price, image=image, category=category, author=author)
            listing.save()
        
        else:
            return render(request, "auctions/create.html", {
                "form": form
            })

    return render(request, "auctions/create.html", {
        "form" : ListingForm
    })


def listing(request, id):
    listing = get_object_or_404(Listing, pk=id)
    comments = listing.comments.all().order_by('-date')
    bids = listing.bids.all()
    max_bid = bids.aggregate(Max('amount'))['amount__max']

    if request.method == "POST":
        
        # Comment validation
        if 'comment' in request.POST:
            comment_form = CommentForm(request.POST)
        
            if comment_form.is_valid():
                author = request.user
                text = comment_form.cleaned_data['text']
                comment = Comment(author=author, text=text, listing=listing)
                
                comment.save()
            else:
                return render(request, "auctions/listing.html", {
                    "comment_form": comment_form,
                    'listing': listing
                })
        
        # Bid validation
        if 'bid' in request.POST:
            bid_form = BidForm(request.POST)

            if bid_form.is_valid():
                author = request.user
                amount = bid_form.cleaned_data['amount']
                bid = Bid(author=author, amount=amount, listing=listing)

                if bid.amount > max_bid:
                    bid.save()
                else:
                    return HttpResponseRedirect(reverse('listing', args=[listing.id]))
        
            else:
                return render(request, "auctions/listing.html", {
                    "bid_form": bid_form,
                    'listing': listing
                })
        
        return HttpResponseRedirect(reverse('listing', args=[listing.id]))

    # GET request
    return render(request, 'auctions/listing.html', {
        'listing' : listing,
        'comments': comments,
        'bids' : bids,
        'max_bid': f'{max_bid:.2f}' if bids else 0,
        'comment_form': CommentForm,
        'bid_form': BidForm
    })


@login_required
def addwatchlist(request, id):
    listing = get_object_or_404(Listing, pk=id)
    user = request.user

    if request.method == 'POST':
        if 'add' in request.POST:
            user.watchlist.add(listing)
        
        if 'remove' in request.POST:
            user.watchlist.remove(listing)
    
    return HttpResponseRedirect(reverse('listing', args=[listing.id]))


@login_required
def watchlist(request):
    user = request.user
    listings = user.watchlist.all().order_by('-date')

    return render(request, "auctions/index.html", {
        "listings" : listings,
        'header': 'Your watchlist'
    })


def categories(request):
    categories = Category.objects.only('name').all()
    try:
        category = Category.objects.get(name=request.GET.get('q'))
        listings = category.listings.all()
    except Category.DoesNotExist:
        listings = Listing.objects.all()
    
    return render(request, "auctions/categories.html", {
        'listings': listings,
        'header': 'Pick category',
        'categories': categories
    }) 
