from django.urls import path
from .views import HelloWorld, LoginView, LogoutView, MyModelList, RegisterView, UserView, AddUserImageView

urlpatterns = [
    path('hello/', HelloWorld.as_view()),
    path('mymodels/', MyModelList.as_view()),
    
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('user/', UserView.as_view()),
    path('user/<int:pk>/image/', AddUserImageView.as_view()),
]