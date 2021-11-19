from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, Group, PermissionsMixin
)
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Group(models.Model):
    name = models.CharField(max_length=200)
        


class User(AbstractBaseUser, PermissionsMixin):

    objects = UserManager()
    
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    meat_mult = models.IntegerField(null=True) 
    car_mult = models.IntegerField(null=True)
    water_mult = models.IntegerField(null=True)
    foodsource_mult = models.IntegerField(null=True) 
    total_points = models.IntegerField(null=True)
    group = models.ForeignKey(Group, null=True, on_delete=models.SET_NULL)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    def __str__(self):              # __unicode__ on Python 2
        return self.email


class CompletedChallenge(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    date_completed = models.DateTimeField(auto_now_add=True)
    total_points = models.IntegerField(null=True)

