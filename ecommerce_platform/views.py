from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.decorators import login_required
from ecommerce_platform.forms import *
from ecommerce_platform.models import *

# Create your views here.


def home_action(request):
    return render(request, 'home.html', {})


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

    new_profile = Profile()
    new_profile.user = new_user
    new_profile.bio_input_text = ""
    new_profile.id = new_user.id
    new_profile.save()
    return redirect(reverse('home'))


