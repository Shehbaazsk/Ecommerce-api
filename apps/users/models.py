from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager

# Create your models here.

class Country(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "country"
        verbose_name_plural = "countries"

class State(models.Model):
    name = models.CharField(max_length=255, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='state')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "state"
        verbose_name_plural = "states"

class City(models.Model):
    name = models.CharField(max_length=255)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='city')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "city"
        verbose_name_plural = "cities"

class UserAddress(models.Model):
    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100, null=True, blank=True)
    address_line_3 = models.CharField(max_length=100, null=True, blank=True)
    locality = models.ForeignKey(City, on_delete=models.CASCADE, related_name='user_address')
    pincode = models.CharField(max_length=6)

    def __str__(self):
        return self.id
    
    class Meta:
        verbose_name = "user_address"
        verbose_name_plural = "user_addresses"

class User(AbstractBaseUser):
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    email=models.EmailField(max_length=255, unique=True)
    mobile_no=models.CharField(max_length=10, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    address = models.ForeignKey(UserAddress, on_delete=models.CASCADE, related_name='user',\
                                null=True, blank=True)
    
    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    objects=UserManager()   

    USERNAME_FIELD = 'email'  

    def __str__(self):
        return self.email
        
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser