# Create your models here.
import datetime
import random
import string
from django.utils.text import slugify
from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save
from django.dispatch import receiver



class Product(models.Model):
    name = models.CharField(max_length=200, unique=True, null=True, blank=True)

    is_active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('product-view')

    def __str__(self):
        return self.name


class Varient(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='items/', null=True, blank=True)
    image2 = models.ImageField(upload_to='items/', null=True, blank=True)
    image3 = models.ImageField(upload_to='items/', null=True, blank=True)
    banner = models.ImageField(upload_to='items/', null=True, blank=True)

    quantity = models.FloatField(default=1)
    brand = models.CharField(null=True, max_length=15)
    description = models.CharField(
        max_length=250, null=True)
    price = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True,null=True)
    stock = models.PositiveIntegerField(default=0,null=True)

    def __str__(self):
        return f"{self.product.name}"

    def get_absolute_url(self):
        return reverse('subproductview')


from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)

        if not kwargs.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not kwargs.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **kwargs)

    def get_by_natural_key(self, email):
        return self.get(email=email)


from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class Users(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, unique=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=128, null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)  # Add this field
    is_anonymous = models.BooleanField(default=False, null=True, blank=True)

    USERNAME_FIELD = 'email'  # specify the username field
    REQUIRED_FIELDS = ['name', ]

    objects = MyUserManager()

    def get_absolute_url(self):
        return reverse('myprofile')

    def __str__(self):
        return self.email

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    @property
    def is_authenticated(self):
        return True if self.pk else False

    @property
    def is_anonymous(self):
        return False

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


class CartItem(models.Model):
    varient = models.ForeignKey(Varient, on_delete=models.CASCADE)
    cart = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    price = models.IntegerField(default=0, null=True, blank=True)



    def __str__(self):
        return str(self.varient.product.name)




    def get_total(self):
        total = self.varient.price * self.quantity
        return total

    def save(self, *args, **kwargs):
        self.price = self.get_total()
        super().save(*args, **kwargs)


class Shipping(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=20, blank=False)
    address = models.CharField(max_length=50, default='', blank=False)
    city = models.CharField(max_length=10, null=True, default='', blank=False)
    pincode = models.CharField(max_length=6)
    phone = models.CharField(max_length=10, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    is_default = models.BooleanField(null=True,blank=True)

    def save(self, *args, **kwargs):
        if self.is_default:
            Shipping.objects.filter(user=self.user).exclude(pk=self.pk).update(is_default=False)
        elif not Shipping.objects.filter(user=self.user, is_default=True).exists():
            self.is_default = True
        super().save(*args, **kwargs)


    def __str__(self):
        if self.name:
            return self.name
        else:
            return f"Shipping record {self.name}"







class Wishlist(models.Model):
    cart = models.ForeignKey(Users, on_delete=models.CASCADE)
    varient = models.ForeignKey(Varient, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)





def generate_order_ids():
    # Generate a 6-character random string with digits and uppercase letters
    return ''.join(random.choices(string.digits + string.ascii_uppercase, k=6))


class Orders(models.Model):
    STATUS_CHOICES = (
        ('confirmed', 'Confirmed'),
        ('placed', 'Placed'),
        ('shipped', 'Shipped'),
        ('cancel','cancel')
    )

    CANCEL_CHOICES = (
        ('Return_approved','Return_approved'),
        ('Return_Rejected', 'Return_Rejected'),
        ('Return_request_accepted','Return_request_accepted')

    )


    order_id = models.CharField(max_length=10, unique=True, null=True)
    user = models.ForeignKey(Users, null=True, on_delete=models.CASCADE)
    items = models.PositiveIntegerField(default=0, null=True, blank=True)
    total_amount = models.PositiveIntegerField(default=0, null=True, blank=True)
    date = models.DateField(default=datetime.datetime.today)
    shipping = models.ForeignKey(Shipping, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,default='confirmed', null=True, blank=True)
    reason = models.CharField(max_length=20,null=True)
    messages = models.CharField(max_length=30, null=True, blank=True)
    approved_by = models.CharField(max_length=30, choices=CANCEL_CHOICES,default='Return_request_accepted')


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.id)  # Slugify the order ID
        super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.order_id:
            # Generate a unique order ID
            while True:
                orderid = generate_order_ids()
                if not Orders.objects.filter(order_id=orderid).exists():
                    break
            self.order_id = orderid
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_id}"


class OrderItems(models.Model):
    quantity = models.FloatField(default=0, null=True, blank=True)
    price = models.PositiveIntegerField(default=0, null=True, blank=True)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, null=True)
    varient = models.ForeignKey(Varient, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False,null=True, blank=True)
    reason = models.CharField(max_length=20, null=True)
    messages  = models.CharField(max_length=30, null=True, blank=True)
    status = models.CharField(max_length=20, default='confirmed', null=True, blank=True)




    def save(self, *args, **kwargs):
        if self.is_completed:
            self.varient.stock -= self.quantity
            self.varient.save()
        super().save(*args, **kwargs)


