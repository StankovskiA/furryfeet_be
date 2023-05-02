from django.urls import path
from .views import HelloWorld, LoginView, LogoutView, MyModelList, RegisterView, UserView, AddUserImageView, DogWalkerView, AppointmentView, FeedbackView, UsersView, DogWalkersView

urlpatterns = [
    path('hello/', HelloWorld.as_view()),
    path('mymodels/', MyModelList.as_view()),
    
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('user/', UserView.as_view()),
    path('user/<int:pk>/image/', AddUserImageView.as_view()),
    path('users/', UsersView.as_view()),
    path('dog_walker/', DogWalkerView.as_view(), name='dog-walker-get'),  # GET request to retrieve dog walker info, appointments and feedbacks
    path('all-dogwalkers/', DogWalkersView.as_view()),
    path('appointments/<int:pk>', AppointmentView.as_view(), name='appointment-get'),  # GET request to retrieve appointments
    path('feedbacks/', FeedbackView.as_view(), name='feedback-get'),  # GET request to retrieve feedbacks
]