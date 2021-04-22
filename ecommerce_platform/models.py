from django.db import models
from django.contrib.auth.models import User


# Create your models here.


# The model for each individual product
class Product(models.Model):
    CATEGORIES = [
        ("Apparel", "Apparel"), 
        ("Pet Supplies", "Pet Supplies"),
        ("Home Goods", "Home Goods"),
        ("Pet Supplies", "Pet Supplies"),
        ("Electronics", "Electronics")
    ]
    # Each product requires three pictures
    product_picture1 = models.ImageField(blank=True)
    product_picture2 = models.ImageField(blank=True)
    product_picture3 = models.ImageField(blank=True)
    # Product info: name, description, price, in_stock_quantity, availability,
    #               category, seller
    product_name = models.CharField(max_length=200)
    product_description = models.CharField(max_length=1000)
    product_price = models.IntegerField()
    product_in_stock_quantity = models.IntegerField()
    product_availability = models.BooleanField(default=True)
    product_category = models.CharField(max_length=50, choices=CATEGORIES)
    product_seller = models.ForeignKey(User, on_delete=models.PROTECT)


# The model for each review for products, use filter to get reviews for each
# product.
class Review(models.Model):
    review_product = models.OneToOneField(Product, on_delete=models.PROTECT)
    review_content = models.CharField(max_length=200)
    review_reviewer = models.ForeignKey(User, on_delete=models.PROTECT)


# The model for each user's wishlist
class Wishlist(models.Model):
    wishlist_products = models.ManyToManyField(Product,
                                               related_name="wishlist_contains")
    wishlist_user = models.OneToOneField(User, on_delete=models.PROTECT)


# The model for each user's shopping cart
class ShoppingCart(models.Model):
    shopping_cart_product = models.ManyToManyField(Product,
                                                   related_name="cart_contains")
    shopping_cart_user = models.OneToOneField(User, on_delete=models.PROTECT)


# The model for user profile
class Profile(models.Model):
    profile_picture = models.FileField(blank=True)
    content_type = models.CharField(max_length=50)
    profile_user = models.ForeignKey(User, on_delete=models.PROTECT,
                                     related_name="profile_user")

    # to get list of selling product: profile.profile_user.product_set.objects.all()

    def __str__(self):
        return 'id=' + str(self.id) + ",pic=" + self.profile_picture.name


# The model for Order
class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.PROTECT,
                              related_name="buyer")
    seller = models.ForeignKey(User, on_delete=models.PROTECT,
                               related_name="seller")
    # one order can contain many products, and a product can be in multiple orders
    item = models.ManyToManyField(Product, related_name="order_contains")
    quantity = models.IntegerField()
    total_price = models.IntegerField()
    ongoing = models.BooleanField()

    def __str__(self):
        return "Order ID: "+str(self.id)+"Ongoing: "+str(self.ongoing)


class PaypalOrder(models.Model):
    # name = models.CharField(max_length=191)
    # email = models.EmailField()
    # postal_code = models.IntegerField()
    # address = models.CharField(max_length=191)
    # date = models.DateTimeField(auto_now_add=True)
    total = models.IntegerField()
    #paid = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.id)

    def total_cost(self):
        return self.total
