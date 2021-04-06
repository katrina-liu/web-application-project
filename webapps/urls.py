"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ecommerce_platform import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_action),
    path('home', views.home_action, name = 'home'),
    path('login', views.login_action, name = 'login'),
    path('register', views.register_action, name='register'),
    path('shopping_cart', views.shopping_cart_action, name='shopping_cart'),
    path('wishlist', views.wishlist_action, name='wishlist'),
    path('profile', views.profile_action, name='profile'),
    path('edit_profile', views.edit_profile, name='edit-profile'),
    path('logout', views.logout_action, name='logout'),
    path('order_buyer', views.order_buyer_action, name='order_buyer'),
    path('order_seller', views.order_seller_action, name='order_seller'),
    path('other_profile_<int:id>', views.other_profile_action,
         name='other_profile'),
    path('product_<int:id>', views.product_action, name="product"),
    path('add_product', views.add_product_action, name='add_product'),
    path('check_out', views.check_out_action, name='check_out')
]
