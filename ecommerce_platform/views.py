from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.decorators import login_required
from ecommerce_platform.forms import *
from ecommerce_platform.models import *
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt



# Create your views here.


def home_action(request):
    context = {}
    context['products'] = Product.objects.all().filter(
        product_availability=True).order_by('-id')
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
    shopping_cart = ShoppingCart.objects.all().get(
        shopping_cart_user=request.user)
    available = shopping_cart.shopping_cart_product.filter(
        product_availability=True)
    other = shopping_cart.shopping_cart_product.filter(
        product_availability=False)
    context['available_products'] = available
    context['unavailable_products'] = other
    context['total_price'] = 0
    for item in available:
        context['total_price'] += item.product_price
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
    # POST Request: update existing profile.
    context = {}
    user = request.user
    context['first_name'] = user.first_name
    context['last_name'] = user.last_name
    context['ProfileForm'] = ProfileForm()

    item = get_object_or_404(Profile, profile_user=user)
    form = ProfileForm(request.POST, request.FILES)
    if not form.is_valid():
        context = {'item': item, 'form': form}
        return render(request, 'profile.html', context)

    item.profile_picture = form.cleaned_data['profile_picture']
    item.content_type = form.cleaned_data['profile_picture'].content_type
    item.save()
    context['message'] = 'Item #{0} saved.'.format(item.id)
    context['ProfileForm'] = ProfileForm()
    context['profile'] = item
    return render(request, 'profile.html', context)


def other_profile_action(request, id):
    context = {}
    # profile = Profile.objects.all().get(id=id)
    profile = get_object_or_404(Profile, id=id)
    context['first_name'] = profile.profile_user.first_name
    context['last_name'] = profile.profile_user.last_name
    context['profile'] = profile
    context['products'] = profile.profile_user.product_set.all()
    return render(request, 'other_profile.html', context)


@login_required
def get_photo(request, id, pid):
    item = get_object_or_404(Product, id=id)
    if pid == 1:
        if not item.product_picture1:
            raise Http404
        else:
            return HttpResponse(item.product_picture1)
    if pid == 2:
        if not item.product_picture2:
            raise Http404
        else:
            return HttpResponse(item.product_picture2)
    if pid == 3:
        if not item.product_picture3:
            raise Http404
        else:
            return HttpResponse(item.product_picture3)


def get_profile_photo(request, id):
    item = get_object_or_404(Profile, id=id)
    if not item.profile_picture:
        raise Http404
    else:
        return HttpResponse(item.profile_picture)


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
    context["products"] = Product.objects.all()
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
    try:
        product = Product.objects.all().get(id=id)
    except:
        return render(request, 'error.html', context)
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
    form = ProductForm(request.POST, request.FILES)
    if form.is_valid():
        p1 = form.cleaned_data['product_picture1']
        p2 = form.cleaned_data['product_picture2']
        p3 = form.cleaned_data['product_picture3']
        product_name = form.cleaned_data['product_name']
        product_description = form.cleaned_data['product_description']
        product_price = form.cleaned_data['product_price']
        product_in_stock_quantity = form.cleaned_data[
            'product_in_stock_quantity']
        product_category = form.cleaned_data['product_category']
        product_availability = (product_in_stock_quantity > 0)
        product_seller = request.user
        product = Product(product_picture1=p1, product_picture2=p2,
                          product_picture3=p3,
                          product_name=product_name,
                          product_description=product_description,
                          product_price=product_price,
                          product_in_stock_quantity=product_in_stock_quantity,
                          product_category=product_category,
                          product_availability=product_availability,
                          product_seller=product_seller)
        product.save()
    return redirect(reverse('home'))

@login_required
def edit_product_action(request, id):
    try:
        product = Product.objects.get(id=id)
    except:
        return render(request, 'error.html')
    context= {}
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        context['form'] = form
        reviews = Review.objects.filter(review_product=product).order_by('-id')
        context['reviews'] = reviews
        if form.is_valid():
            p = form.save(commit=False)
            p.product_seller = request.user
            p.save()
            context['product'] = p
            return render(request, 'product.html', context)
    else:
        form = ProductForm(instance=product)
        context['form'] = form
    return render(request, 'add_product.html', context)

@login_required
def delete_product_action(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect(reverse('home'))


def check_out_action(request):
    context = {}
    shopping_cart_products = ShoppingCart.objects.all().get(
        shopping_cart_user=request.user).shopping_cart_product
    available_products = shopping_cart_products.filter(
        product_availability=True)
    cost = 0
    for product in available_products:
        product.product_availability = False
        new_order = Order()
        new_order.buyer = request.user
        new_order.seller = product.product_seller
        new_order.quantity = 1
        new_order.total_price = product.product_price
        new_order.ongoing = True
        new_order.save()
        new_order.item.add(product)
        product.product_in_stock_quantity -= 1
        cost += product.product_price
        if product.product_in_stock_quantity > 0:
            product.product_availability = True
        shopping_cart_products.remove(product)
    paypal_order = PaypalOrder(total=cost)
    paypal_order.save()
    request.session['order_id'] = paypal_order.id
    return redirect(reverse('process_payment'))


def change_category(request, category):
    context = {}
    context['products'] = Product.objects.all().filter(
        product_category=category).order_by('-id')
    return render(request, 'home.html', context)


def buy_change_ongoing(request, ongoing):
    context = {}
    if ongoing == 1:
        order_ongoing = True
        order_list = Order.objects.all().filter(buyer=request.user,
                                                ongoing=True)
    else:
        order_ongoing = False
        order_list = Order.objects.all().filter(buyer=request.user,
                                                ongoing=False)
    context['ongoing'] = order_ongoing
    context['order_list'] = order_list
    context["products"] = Product.objects.all()
    return render(request, 'order_buyer.html', context)


def sell_change_ongoing(request, ongoing):
    context = {}
    if ongoing == 1:
        order_list = Order.objects.all().filter(seller=request.user,
                                                ongoing=True)
    else:
        order_list = Order.objects.all().filter(seller=request.user,
                                                ongoing=False)
    context['order_list'] = order_list
    context["products"] = Product.objects.all()
    return render(request, 'order_seller.html', context)


def add_to_shopping_cart(request, product_id):
    shopping_cart = ShoppingCart.objects.all().get(
        shopping_cart_user=request.user)
    shopping_cart.shopping_cart_product.add(
        Product.objects.all().get(id=product_id))
    return redirect(reverse('shopping_cart'))


def add_to_wish_list(request, product_id):
    wishlist = Wishlist.objects.all().get(wishlist_user=request.user)
    wishlist.wishlist_products.add(Product.objects.all().get(id=product_id))
    return redirect(reverse('wishlist'))


def move_wishlist_to_cart(request, id):
    user = request.user
    product = get_object_or_404(Product, id=id)
    wishlist = get_object_or_404(Wishlist, wishlist_user=user)
    cart = get_object_or_404(ShoppingCart, shopping_cart_user=user)
    # delete item from wishlist
    wishlist.wishlist_products.remove(product)
    # add item to shopping cart
    cart.shopping_cart_product.add(product)
    return redirect(reverse('shopping_cart'))


def move_cart_to_wishlist(request, id):
    user = request.user
    product = get_object_or_404(Product, id=id)
    wishlist = get_object_or_404(Wishlist, wishlist_user=user)
    cart = get_object_or_404(ShoppingCart, shopping_cart_user=user)
    # delete item from shopping cart
    cart.shopping_cart_product.remove(product)
    # add item to wishlist
    wishlist.wishlist_products.add(product)
    return redirect(reverse('wishlist'))

def remove_product_from_wishlist(request, id):
    user = request.user
    product = get_object_or_404(Product, id=id)
    wishlist = get_object_or_404(Wishlist, wishlist_user=user)
    # delete item from wishlist
    wishlist.wishlist_products.remove(product)
    return redirect(reverse('wishlist'))

def remove_product_from_cart(request, id):
    user = request.user
    product = get_object_or_404(Product, id=id)
    cart = get_object_or_404(ShoppingCart, shopping_cart_user=user)
    # delete item from cart
    cart.shopping_cart_product.remove(product)
    return redirect(reverse('shopping_cart'))

def clear_shopping_cart(request):
    user = request.user
    cart = get_object_or_404(ShoppingCart, shopping_cart_user=user)
    cart.shopping_cart_product.clear()
    return redirect(reverse('shopping_cart'))

def clear_wishlist(request):
    user = request.user
    wishlist = get_object_or_404(Wishlist, wishlist_user=user)
    wishlist.wishlist_products.clear()
    return redirect(reverse('wishlist'))

def cancel_order(request, id):
    order = Order.objects.all().get(id=id)
    for product in order.item.all():
        product.product_in_stock_quantity += 1
    order.delete()
    return redirect(reverse('order_buyer'))

def confirm_order(request, id):
    order = Order.objects.all().get(id=id)
    order.ongoing = False
    print(order)
    order.save()
    return redirect(reverse('order_buyer'))


def review_action(request, id):
    context = {}
    try:
        product = Product.objects.get(id=id)
    except:
        return render(request, 'error.html')
    context['product'] = product
    # for all reviews for this product, check if user already reviewed
    numReviews = Review.objects.filter(review_product_id = id, review_reviewer=request.user).count()
    context['hasReviewd'] = True if numReviews!=0 else False
    if request.method == "GET":
        form = ReviewForm
        context['form'] = form
        return render(request, 'review.html', context)
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = Review(review_product=product, review_content=form.cleaned_data['review_content'],
                        review_reviewer=request.user)
        review.save()
    return render(request, 'product.html', context)

def process_payment(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(PaypalOrder, id=order_id)
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%d' % order.total_cost(),
        'item_name': 'Order {}'.format(order.id),
        'invoice': str(order.id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('payment_cancelled')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'process_payment.html', {'order': order, 'form': form})

@csrf_exempt
def payment_done(request):
    context = {}
    order_list = Order.objects.all().filter(buyer=request.user, ongoing=True)
    context['order_list'] = order_list
    context["products"] = Product.objects.all()
    print(context['order_list'])
    return render(request, 'payment_done.html', context)

@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment_cancelled.html')

def error_action(request):
    return render(request, 'error.html')