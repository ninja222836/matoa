import uuid
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_resized import ResizedImageField

from mstore.fields import WEBPField

MODEL_CHOICES = (('EBONY', 'ebony'),
                 ('MAPLE', 'maple'),
                 ('FEATURED', 'featured'))

def image_folder(instance, filename):
    return 'photos/product_images/{}.webp'.format(uuid.uuid4().hex)

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    description_for_slider = models.TextField(null=True, blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_edited = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    category = models.ForeignKey('ProductCategory', on_delete=models.PROTECT)
    new = models.BooleanField(default=False)
    hit = models.BooleanField(default=False)
    model = models.CharField(choices=MODEL_CHOICES, max_length=10, blank=True, default='EBONY')
    related_product = models.OneToOneField('Product', on_delete=models.PROTECT, blank=True, null=True)
    card_image = models.ImageField(upload_to="photos/product_images/%Y/%m/%d/")
    card_image_webp = WEBPField(verbose_name='Card Image', upload_to=image_folder,)

    main_image = models.ImageField(upload_to="photos/product_images/%Y/%m/%d/")
    main_image_webp = WEBPField(verbose_name='Main Image webp', upload_to=image_folder,)

    pid = models.AutoField(primary_key=True)

    favourites = models.ManyToManyField('Customer', related_name='favourite', default=None, blank=True)


    price = models.IntegerField()
    discount = models.IntegerField()
    discounted_price = models.IntegerField(null=True)
    sell_price = models.IntegerField(null=True)



    @property
    def discounted_price(self):
        return ((self.price) * (self.discount)) / 100

    @property
    def sell_price(self):
        return (self.price) - (self.discounted_price)



    def __str__(self):
        return self.name


class ProductImage(models.Model):
    p_image = models.ImageField(upload_to="photos/product_images/%Y/%m/%d/")
    image_webp = ResizedImageField(force_format="WEBP", quality=75, upload_to="photos/product_images/%Y/%m/%d/")
    product = models.ForeignKey("Product", on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name


class ProductColor(models.Model):
    color = models.CharField(max_length=255)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)


class ProductCategory(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name


class ProductScheme(models.Model):
    scheme_image = models.ImageField(upload_to="photos/product_images/%Y/%m/%d/")
    scheme_image_webp = ResizedImageField(force_format="WEBP", quality=75, upload_to="photos/product_images/%Y/%m/%d/")
    product = models.ForeignKey("Product", on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name


class Customer(models.Model):
    title = models.CharField(max_length=200, default='')
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)

    email = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    @receiver(post_save, sender=User)
    def create_user_customer(sender, instance, created, **kwargs):
        if created:
            Customer.objects.create(user=instance, title=instance.username, email=instance.email)

    @receiver(post_save, sender=User)
    def save_user_customer(sender, instance, **kwargs):
        instance.customer.save()


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.pk)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = round(sum([item.get_total for item in orderitems]), 2)
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.name}, {self.order.customer.title}'

    @property
    def get_total(self):
        total = round(self.product.sell_price * self.quantity, 2)
        return total


class Testimonials(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    image = models.ImageField(upload_to="photos/testimonials/%Y/%m/%d/")

