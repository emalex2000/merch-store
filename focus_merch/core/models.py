from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from user_auth_app.models import User
from datetime import datetime


STATUS_CHOICES = (
    ('process', 'Processing'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
)
STATUS = (
    ('draft', 'Draft'),
    ('disabled', 'Rejected'),
    ('in_review', 'In_Review'),
    ('published', 'Published'),
)
RATINGS = (
    (1, '★☆☆☆☆'),
    (2, '★★☆☆☆'),
    (3, '★★★☆☆'),
    (4, '★★★★☆'),
    (5, '★★★★★'),
)

def user_media_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename) #to create media directory for newly created user

class Category(models.Model):
    mycat_id = ShortUUIDField(unique=True, length=10, max_length=30, prefix="cat", alphabet="abcdefghijkz1234567890")
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=user_media_path, default='category.jpg')

    class meta:
        verbose_name_plural = "Categories"

    def category_image(self):
        return mark_safe('<img src="%s" width="50%">' % (self.image.url))
    
    def __str__(self):
        return self.title
    
class Vendor(models.Model):
    vendor_id = ShortUUIDField(unique=True, length=10, max_length=30, prefix="ven", alphabet="abcdefghijkz1234567890")
    title = models.CharField(max_length=100, default='beautyInc')
    image = models.ImageField(upload_to=user_media_path, default='vendor.jpg')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    description =  models.TextField(null=True, blank=True)
    contact = models.CharField(max_length=100, default="123 blessed ave")
    shipping_on_time = models.DateTimeField(auto_now_add=True)
    authentication_ratings = models.CharField(max_length=100, default="100")
    days_return = models.CharField(max_length=100, default="100")
    warranty_period = models.CharField(max_length=100, default="100 days")

    class meta:
        verbose_name_plural = "Vendors"

    def vendor_image(self):
        return mark_safe('<img src="%s" width="50%" height="50%">' % (self.image.url))


    def __str__(self):
        return self.title
    
class Tags(models.Model):
    pass

class Product(models.Model):
    product_id = ShortUUIDField(unique=True, length=10, max_length=30, prefix="prd", alphabet="abcdefghijkz1234567890")
    title = models.CharField(max_length=100, default='ps5')
    description =  models.TextField(null=True, blank=True, default="the latest ps5 could render a high graphic experience")
    price = models.DecimalField(max_digits=999, decimal_places=2, default='10.99')
    prev_price = models.DecimalField(max_digits=999, decimal_places=2, default='20.99')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)                                                                                                                                                                                                                                                                                                                                                                                              
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to=user_media_path, default='product.jpg')
    specifications = models.TextField(null=True, blank=True)
    tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)
    product_status = models.CharField(max_length=10, choices=STATUS, default='in_review')
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    degital = models.BooleanField(default=False)
    sku = ShortUUIDField(unique=True, length=4, max_length=10, prefix="sku", alphabet="1234567890")
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)

    class meta:
        verbose_name_plural = "Products"

    def product_image(self):
        return mark_safe('<img src="%s" width="50%" height="50%">' % (self.image.url))


    def __str__(self):
        return self.title
    
    def get_percentage_discount(self):
        new_price = (self.price/self.prev_price)*100
        return new_price
    
class ProductImages(models.Model):
    images = models.ImageField(upload_to='product-images', default='product.jpg')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class meta:
        verbose_name_plural = "Products Images"







class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=999, decimal_places=2)
    price_stats = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICES, max_length=30, default='processing')

    class meta:
        verbose_name_plural = "Cart Order"


class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0 )
    price = models.DecimalField(max_digits=999, decimal_places=2, default='1.99')
    total = models.DecimalField(max_digits=999, decimal_places=2, default='1.99')

    class meta:
        verbose_name_plural = "Cart Order Items"
    
    def order_image(self):
        return mark_safe('<img src="/media/%s" width="50%" height="50%">' % (self.image.url))
    



class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    review = models.TextField()
    ratings = models.IntegerField(choices=RATINGS, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class meta:
        verbose_name_plural = "Product Reviews"

    def __str__(self):
        return self.product.title
    
    def get_rating(self):
        return self.ratings
    
class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)

    class meta:
        verbose_name_plural = "Wishlist"

    def __str__(self):
        return self.product.title

class Address(models.Model):
    user = models.ForeignKey(User, models.SET_NULL, null=True)
    address = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)

    class meta:
        verbose_name_plural = "Address"

    