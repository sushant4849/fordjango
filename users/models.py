from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.safestring import mark_safe
from django.core.validators import RegexValidator, MaxValueValidator
from shop.models import DeliveryPoint
import random



class UserManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, phone, password, **extra_fields):
        """Create and save a User with the given phone and password."""
        if not phone:
            raise ValueError('The given phone must be set')
        self.phone = phone
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        """Create and save a regular User with the given phone and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        """Create and save a SuperUser with the given phone and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)

class UserCustom(AbstractUser):
    username = None
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(('phone number'), validators=[phone_regex], max_length=17, unique=True) # validators should be a list
    city = models.CharField(max_length=50, blank = True, null=True)
    area = models.CharField(max_length=50, blank = True, null = True)
    delivery_point = models.ForeignKey(DeliveryPoint, on_delete=models.CASCADE, null=True, blank=True)
    pin = models.PositiveIntegerField(null = True, blank = True, validators=[MaxValueValidator(9999)], default = random.randint(1000,9999))
    text_1 = models.CharField(max_length=255, blank = True, null = True)
    text_2 = models.CharField(max_length=255, blank = True, null = True)
    text_3 = models.CharField(max_length=255, blank = True, null = True)
    text_4 = models.CharField(max_length=255, blank = True, null = True)
    text_5 = models.CharField(max_length=255, blank = True, null = True)
    text_6 = models.CharField(max_length=255, blank = True, null = True)
    text_7 = models.CharField(max_length=255, blank = True, null = True)
    text_8 = models.CharField(max_length=255, blank = True, null = True)
    text_9 = models.CharField(max_length=255, blank = True, null = True)
    text_10 = models.CharField(max_length=255, blank = True, null = True)
    text_11 = models.CharField(max_length=255, blank = True, null = True)
    text_12 = models.CharField(max_length=255, blank = True, null = True)
    text_13 = models.CharField(max_length=255, blank = True, null = True)
    text_14 = models.CharField(max_length=255, blank = True, null = True)
    text_15 = models.CharField(max_length=255, blank = True, null = True)
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    def image_tag(self):
        return mark_safe(f"<img src = '{self.image.url}' height = '50' />")

    @property
    def full_name(self):
        
        return f"{self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        self.set_password(str(self.pin))
        super().save(*args, **kwargs)

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    name = models.CharField(max_length=50, blank = True, null = True)
    address = models.CharField(max_length = 255, null = True)
    country = models.CharField(max_length=25, null = True)
    phone = PhoneNumberField(null = True)
    country = models.CharField(max_length=25, null = True)
    company = models.CharField(max_length=60, null = True)
    
    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = "Users' Addresses"
    
    def __str__(self):
        return f"{self.user} Address " 