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
    path('home', views.home_action, name='home'),
    path('login', views.login_action, name='login'),
    path('register', views.register_action, name='register'),
    path('shopping_cart', views.shopping_cart_action, name='shopping_cart'),
    path('wishlist', views.wishlist_action, name='wishlist'),
    path('profile', views.profile_action, name='profile'),
    path('edit_profile', views.edit_profile, name='edit-profile'),
    path('logout', views.logout_action, name='logout'),
    path('order_buyer', views.order_buyer_action, name='order_buyer'),
    path('order_seller', views.order_seller_action, name='order_seller'),
    path('other_profile/<int:id>', views.other_profile_action,
         name='other_profile'),
    path('product_<int:id>', views.product_action, name="product"),
    path('add_product', views.add_product_action, name='add_product'),
    path('edit_product/<int:id>', views.edit_product_action, name='edit_product'),
    path('delete_product/<int:id>', views.delete_product_action, name='delete_product'),
    path('check_out', views.check_out_action, name='check_out'),
    path('get_photo/<int:id>/<int:pid>', views.get_photo, name='photo'),
    path('category=<str:category>', views.change_category, name='category'),
    path('order_sell=<int:ongoing>', views.sell_change_ongoing,
         name='order_sell'),
    path('order_buy=<int:ongoing>', views.buy_change_ongoing, name='order_buy'),
    path('add_to_wishlist=<int:product_id>', views.add_to_wish_list,
         name='add_to_wishlist'),
    path('add_to_shopping_cart=<int:product_id>', views.add_to_shopping_cart,
         name='add_to_shopping_cart'),
    path('get_profile_photo/<int:id>', views.get_profile_photo, name = "profile_photo"),
    path('move_wishlist_to_cart/<int:id>', views.move_wishlist_to_cart, name = "move_wishlist_to_cart"),
    path('move_cart_to_wishlist/<int:id>', views.move_cart_to_wishlist, name = "move_cart_to_wishlist"),
    path('remove_product_from_wishlist/<int:id>', views.remove_product_from_wishlist, name = "remove_product_from_wishlist"),
    path('remove_product_from_cart/<int:id>', views.remove_product_from_cart, name = "remove_product_from_cart"),
    path('clear_shopping_cart', views.clear_shopping_cart, name = "clear_shopping_cart"),
    path('clear_wishlist', views.clear_wishlist, name = "clear_wishlist"),
    path('cancel_order=<int:id>', views.cancel_order, name="cancel_order"),
    path('confirm_order=<int:id>', views.confirm_order, name='confirm_order'),
    path('review/<int:id>', views.review_action, name='review')
]
