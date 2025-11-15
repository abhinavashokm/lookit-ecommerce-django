from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = None # remove username field
    email = models.EmailField(unique=True)
    
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
    
    def __str__(self):
        return self.email