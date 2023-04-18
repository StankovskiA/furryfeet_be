from django.urls import path
from .views import HelloWorld, MyModelList

urlpatterns = [
    path('hello/', HelloWorld.as_view()),
    path('mymodels/', MyModelList.as_view()),
]