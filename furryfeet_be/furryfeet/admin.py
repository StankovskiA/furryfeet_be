from django.contrib import admin
from .models import MyModel, User, DogDetails, Feedback

# Register your models here.
admin.site.register(MyModel)
admin.site.register(User)
admin.site.register(DogDetails)
admin.site.register(Feedback)