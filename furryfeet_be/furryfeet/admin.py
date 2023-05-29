from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Feedback)
admin.site.register(Dog)
admin.site.register(DogFeedback)
admin.site.register(Appointment)
