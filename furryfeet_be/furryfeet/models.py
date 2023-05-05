from django.contrib.auth.models import AbstractUser
from django.db import models

RATING_CHOICES = (
    (1, "1"),
    (2, "2"),
    (3, "3"),
    (4, "4"),
    (5, "5"),
)


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
    is_dog_walker = models.BooleanField(default=False)
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Feedback(models.Model):
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    user_from = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="feedback_given",
        limit_choices_to={"is_dog_walker": False},
    )
    user_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="feedback_received",
        limit_choices_to={"is_dog_walker": True},
    )


class Dog(models.Model):
    name = models.CharField(max_length=50)
    breed = models.CharField(max_length=50)
    age = models.IntegerField()
    tag = models.CharField(max_length=50, unique=True)
    photo = models.URLField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dogs_owned")


class DogFeedback(models.Model):
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    dog_walker = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={"is_dog_walker": True}
    )
    dog = models.ForeignKey(
        Dog, on_delete=models.CASCADE, related_name="feedback_received"
    )


class Appointment(models.Model):
    date = models.DateTimeField()
    dog_walker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="appointments_owned",
        limit_choices_to={"is_dog_walker": True},
    )
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
