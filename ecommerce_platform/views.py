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
    context['products'] = Product.objects.all()
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
    return redirect(reverse('home'))

def shopping_cart_action(request):
    return render(request, 'shopping_cart.html', {})

def wishlist_action(request):
    return render(request, 'wishlist.html', {})

def profile_action(request):
    context = {}
    user = request.user
    context['first_name'] = user.first_name    
    context['last_name'] = user.last_name
    context['ProfileForm'] = ProfileForm()

    # GET Request: Display bio, picture, and form
    if request.method == 'GET':
        userProfile = get_object_or_404(Profile, profile_user=user)
        context['profile'] = userProfile
        return render(request, 'profile.html', context)

def logout_action(request):
    logout(request)
    return redirect(reverse('login'))


