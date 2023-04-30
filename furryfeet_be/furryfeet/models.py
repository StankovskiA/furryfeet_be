from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class MyModel(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name
    
class User(AbstractUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=20)
    joined_at = models.DateTimeField(auto_now_add=True)
    image = models.URLField(null=True, blank=True)
    username = None
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []