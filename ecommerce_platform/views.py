from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.decorators import login_required
from ecommerce_platform.forms import *
from ecommerce_platform.models import *
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404


# Create your views here.


def home_action(request):
    context = {}
    context['products'] = Product.objects.all().order_by('-id')
    return render(request, 'home.html', context)


def login_action(request):
    context = {}

    if request.method == "GET":
        context["form"] = LoginForm()
        return render(request, 'login.html', context)

    form = LoginForm(request.POST)
    context["form"] = form
    if not form.is_valid():
        return render(request, "login.html", context)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])
    login(request, new_user)
    return redirect(reverse('home'))


def register_action(request):
    context = {}

    if request.method == "GET":
        context["form"] = RegisterForm()
        return render(request, 'register.html', context)

    form = RegisterForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'register.html', context)

    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data[
                                            'first_name'],
                                        last_name=form.cleaned_data[
                                            'last_name'])

    new_user.save()

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])
    login(request, new_user)
    new_profile = Profile(profile_user=new_user)
    profileForm = ProfileForm(request.POST, request.FILES, instance=new_profile)
    new_profile.save()
    shopping_cart = ShoppingCart(shopping_cart_user=new_user)
    wishlist = Wishlist(wishlist_user=new_user)
    shopping_cart.save()
    wishlist.save()
    return redirect(reverse('home'))


@login_required
def shopping_cart_action(request):
    context = {}
    shopping_cart = ShoppingCart.objects.all().get(shopping_cart_user=request.user)
    available = shopping_cart.shopping_cart_product.filter(product_availability=True)
    other = shopping_cart.shopping_cart_product.filter(product_availability=False)
    context['available_products'] = available
    context['unavailable_products'] = other
    return render(request, 'shopping_cart.html', context)


@login_required
def wishlist_action(request):
    context = {}
    wishlist = Wishlist.objects.all().get(wishlist_user=request.user)
    available = wishlist.wishlist_products.filter(product_availability=True)
    other = wishlist.wishlist_products.filter(product_availability=False)
    context['available_products'] = available
    context['unavailable_products'] = other
    return render(request, 'wishlist.html', context)


@login_required
def profile_action(request):
    context = {}
    user = request.user
    context['first_name'] = user.first_name
    context['last_name'] = user.last_name
    context['ProfileForm'] = ProfileForm()
    context['products'] = user.product_set.all()

    # GET Request: Display bio, picture, and form
    if request.method == 'GET':
        userProfile = get_object_or_404(Profile, profile_user=user)
        context['profile'] = userProfile
        return render(request, 'profile.html', context)

@login_required
def edit_profile(request):
    #POST Request: update existing profile.
    context = {}
    user = request.user
    context['first_name'] = user.first_name    
    context['last_name'] = user.last_name
    context['ProfileForm'] = ProfileForm()

    item = get_object_or_404(Profile, profile_user=user)
    form = ProfileForm(request.POST, request.FILES)
    if not form.is_valid():
        context = { 'item': item, 'form': form }
        return render(request, 'profile.html', context)
    
    pic = form.cleaned_data['profile_picture']
    item.profile_picture = form.cleaned_data['profile_picture']
    item.content_type = form.cleaned_data['profile_picture'].content_type
    item.save()
    context['message'] = 'Item #{0} saved.'.format(item.id)
    context['ProfileForm'] = ProfileForm()
    context['profile'] = item
    return render(request, 'profile.html', context)


def other_profile_action(request, id):
    context = {}
    profile = Profile.objects.all().get(id=id)
    context['first_name'] = profile.first_name
    context['last_name'] = profile.last_name
    return render(request, 'other_profile.html', context)


@login_required
def logout_action(request):
    logout(request)
    return redirect(reverse('login'))


@login_required
def order_buyer_action(request):
    context = {}
    order_type = 'ongoing'
    order_list = Order.objects.all().filter(buyer=request.user, ongoing=True)
    context['order_list'] = order_list
    return render(request, 'order_buyer.html', context)


@login_required
def order_seller_action(request):
    context = {}
    order_type = 'ongoing'
    context['order_type'] = order_type
    order_list = Order.objects.all().filter(seller=request.user, ongoing=True)
    context['order_list'] = order_list
    return render(request, 'order_seller.html', context)


def product_action(request, id):
    context = {}
    product = Product.objects.all().get(id)
    context['product'] = product
    reviews = Review.objects.filter(review_product=product).order_by('-id')
    context['reviews'] = reviews
    return render(request, 'product.html', context)


@login_required
def add_product_action(request):
    context = {}
    if request.method == 'GET':
        context['form'] = ProductForm
        return render(request, 'add_product.html', context)
    new_product = Product(request.POST, request.FILES)
    new_product.product_availability = True
    new_product.product_seller = request.user
    new_product.save()
    return reverse(redirect('home'))


def check_out_action(request):
    context = {}
    return render(request, 'transaction.html', context)

