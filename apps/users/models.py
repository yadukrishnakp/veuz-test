from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from .validators import validate_possible_number
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext as _
from django_acl.models import Group,Role
from django.utils.text import slugify
from random import randint
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    Permission,
    PermissionsMixin,
)

# Create your models here
class PossiblePhoneNumberField(PhoneNumberField):
    """Less strict field for phone numbers written to database."""
    default_validators = [validate_possible_number]

def users_image(self, filename):
    return f"users/{self.id}/{self.username}-{self.email}.png"

def users_default_image():
    return f"default/avatar/default-user-image.jpg"

class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password = None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))

        email = self.normalize_email(email)
        user = self.model(email = email, **extra_fields)
        if password:
            user.set_password(password)
            
        user.save()
        return user


    def create_superuser(self, email, password,**extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('is_admin', True)
    
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff = True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser = True.'))
        
        return self.create_user(email, password, **extra_fields)


class Users(AbstractBaseUser, PermissionsMixin):
    USER_TYPES = [
        ('1', 'Admin'),
        ('2', 'Customer'),
    ]        
    user_type           = models.CharField(max_length=100,choices=USER_TYPES, blank=True, null=True)
    email               = models.EmailField(_('Email'), max_length = 255, unique = True, blank = True, null = True)
    full_name           = models.CharField(_('Full Name'), max_length = 200, blank = True, null = True)
    username            = models.CharField(max_length=256, blank=True)
    date_joined         = models.DateTimeField(_('Date Joined'),  auto_now_add = True, blank = True, null = True)
    last_login          = models.DateTimeField(_('Last Login'),  auto_now = True, blank = True, null = True)
    is_verified         = models.BooleanField(default = True)
    is_admin            = models.BooleanField(default = False)
    is_active           = models.BooleanField(default = True)
    is_staff            = models.BooleanField(default = False)
    is_superuser        = models.BooleanField(default = False)
    slug                = models.SlugField(max_length=256, unique=True, editable=False, blank = True, null = True)
    user_groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='custom_group_set',
        related_query_name='custom_group',
    )


    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='custom_permission_set',  # Add or change the related_name here
        related_query_name='custom_permission',
    )


    USERNAME_FIELD = 'email'

    # REQUIRED_FIELDS = ['email','password']

    objects = UserManager()
    # slug for User table with releated to first name
    def save(self, *args, **kwargs):
        if not self.slug or self.email:
            self.slug = slugify(str(self.email))
            if Users.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = slugify(str(self.email)) + '-' + str(randint(1, 9999999))
        super(Users, self).save(*args, **kwargs)
        

    def __str__(self):
        return self.email

    