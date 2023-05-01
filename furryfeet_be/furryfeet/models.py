from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class MyModel(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name

class DogDetails(models.Model):
    name = models.CharField(max_length=50)
    breed = models.CharField(max_length=50)
    age = models.IntegerField()
    dog_id = models.CharField(max_length=50)
    feedbacks = models.TextField()
    dog_photo = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=20)
    joined_at = models.DateTimeField(auto_now_add=True)
    image = models.URLField(null=True, blank=True)
    username = models.CharField(max_length=20,blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]
    dog_details = models.ForeignKey(DogDetails, on_delete=models.CASCADE, null=True, blank=True)


class Feedback(models.Model):
    RATING_CHOICES = (
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Average'),
        (4, '4 - Good'),
        (5, '5 - Excellent')
    )

    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    sender = models.ForeignKey(User, related_name='sent_feedback', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_feedback', on_delete=models.CASCADE)