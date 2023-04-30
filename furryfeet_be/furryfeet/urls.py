from django.urls import path
from .views import HelloWorld, LoginView, LogoutView, MyModelList, RegisterView, UserView, AddUserImageView,DogWalkerView,AppointmentView,FeedbackView

urlpatterns = [
    path('hello/', HelloWorld.as_view()),
    path('mymodels/', MyModelList.as_view()),
    
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('user/', UserView.as_view()),
    path('user/<int:pk>/image/', AddUserImageView.as_view()),
    path('dog-walker/', DogWalkerView.as_view(), name='dog-walker-get'),  # GET request to retrieve dog walker info, appointments and feedbacks
    path('dog-walker/<int:pk>/', DogWalkerView.as_view(), name='dog-walker-update'),  # POST request to update dog walker info
    path('appointments/', AppointmentView.as_view(), name='appointment-get'),  # GET request to retrieve appointments
    path('appointments/<int:pk>/', AppointmentView.as_view(), name='appointment-create'),  # POST request to create a new appointment
    path('feedbacks/', FeedbackView.as_view(), name='feedback-get'),  # GET request to retrieve feedbacks
    path('feedbacks/<int:pk>/', FeedbackView.as_view(), name='feedback-create'),  # POST request to create a new feedback
]