from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings

# Model with fields created for profile page
class Profile(models.Model):
    GENDER = (
        ('male', 'Male'),
        ('female', 'Female'),)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_img = models.ImageField(default='default.jpg', upload_to='Profile Image/')
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(max_length=20,choices=GENDER)
    about = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.full_name} Profile'

#added a custom Manager, by subclassing BaseUserManager, that uses an email as the unique identifier instead of a username.
class UserManager(BaseUserManager):

    # sets what kind of information is needed when the user is created 
    def create_user(
            self, email, full_name, password=None,
            commit=True):
        """
        Creates and saves a User with the given email, full name
        and password.
        """
        if not email:
            raise ValueError(_('Users must have an email address'))
        if not full_name:
            raise ValueError(_('Users must have a full_name'))
       

        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            
        )

        user.set_password(password)
        if commit:
            user.save(using=self._db)
        return user

    #sets what kind of information is needed while created superuser(admin)
    def create_superuser(self, email, full_name, password):
        """
        Creates and saves a superuser with the given email, first name,
        last name and password.
        """
        user = self.create_user(
            email,
            password=password,
            full_name=full_name,
            commit=False,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# Created a new class called CustomUser that subclasses AbstractUser
# Added fields for email, is_staff, is_active, and date_joined
# Set the USERNAME_FIELD -- which defines the unique identifier for the User model -- to email
# Specified that all objects for the class come from the CustomUserManager
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name=_('email address'), max_length=255, unique=True
    )
    # password field supplied by AbstractBaseUser
    # last_login field supplied by AbstractBaseUser
    full_name = models.CharField(_('full_name'), max_length=30, blank=True)
   
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        ),
    )
    # is_superuser field provided by PermissionsMixin
    # groups field provided by PermissionsMixin
    # user_permissions field provided by PermissionsMixin

    date_joined = models.DateTimeField(
        _('date joined'), default=timezone.now
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def get_full_name(self):
       
        full_name = '%s' % (self.full_name)
        return full_name.strip()

    def __str__(self):
        return self.full_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
