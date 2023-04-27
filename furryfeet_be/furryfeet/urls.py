from django.urls import path
from .views import HelloWorld, LoginView, LogoutView, MyModelList, RegisterView, UserView

urlpatterns = [
    path('hello/', HelloWorld.as_view()),
    path('mymodels/', MyModelList.as_view()),
    
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('user/', UserView.as_view()),
]