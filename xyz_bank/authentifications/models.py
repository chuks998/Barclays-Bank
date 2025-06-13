from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django_countries.fields import CountryField
from django.utils.timezone import now
import random

class CustomUserManager(BaseUserManager):
    def create_user(self, name, email, country, username, password=None):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(name=name, email=email, country=country, username=username)
        user.set_password(password)
        user.is_active = False  # Inactive until email verification
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, country, username, password):
        user = self.create_user(name, email, country, username, password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    country = CountryField(blank_label="Select Country")
    username = models.CharField(unique=True, max_length=50)
    account_number = models.CharField(max_length=10, unique=True, blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    profile_picture = models.ImageField(
        upload_to="profile_pics/", 
        default="default_profile.jpg", 
        blank=True, 
        null=True
    )
    account_ready = models.BooleanField(default=False)  # Determines if the user can withdraw
    is_active = models.BooleanField(default=False)  # Becomes active after email verification
    is_staff = models.BooleanField(default=False)  # Restricts admin access
    date_joined = models.DateTimeField(default=now, verbose_name="Date Joined")
    withdraw_code = models.CharField(max_length=6, unique=True, blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "country", "username"]

    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = self.generate_account_number()
        if not self.withdraw_code:
            self.withdraw_code = self.generate_withdraw_code()
        super().save(*args, **kwargs)

    def generate_account_number(self):
        return str(random.randint(1000000000, 9999999999))  # 10-digit unique account number

    def generate_withdraw_code(self):
        return str(random.randint(100000, 999999))  # 6-digit unique code

    def __str__(self):
        return self.name
