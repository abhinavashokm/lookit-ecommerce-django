from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

#Creating custom user manager
class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None # remove username field
    email = models.EmailField(unique=True)
    
    #will not use these fields, just making them harmless
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, null=True, blank=True )
    gender = models.CharField(max_length=10, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)

    referral_code = models.CharField(max_length=50 ,unique=True)
    referred_by = models.CharField(max_length=50, null=True, blank=True)
    referral_reward = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    status = models.CharField(max_length=10, default="Active")
    updated_at = models.DateField(auto_now=True)
    
    #Use email as the unique identifier for login instead of username.
    USERNAME_FIELD = 'email'
    
    #When creating superuser, don't ask for anything extra besides email + password
    REQUIRED_FIELDS = []
    
    #set custom user manager, becuase we are using email for authentication
    objects = UserManager()
    
    def __str__(self):
        return self.email