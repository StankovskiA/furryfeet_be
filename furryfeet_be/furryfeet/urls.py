from django.urls import path
from .views import *

urlpatterns = [
    path('hello/', HelloWorld.as_view()),
    path('mymodels/', MyModelList.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('user/', UserView.as_view()),
    path('user/alldogwalkers/',GetAllDogWallkers.as_view()),
    path('user/dogwalker/<int:id>', GetDogWallkerById.as_view()),
    path('user/change-password/', ChangeUserPasswordView.as_view()), #password change for the currently logged in user
    path('user/<int:pk>/image/', AddUserImageView.as_view()),
    path('feedback/all-feedbacks/', FeedbackListView.as_view()), #listing all feedbacks
    path('feedback/create-feedback/', FeedbackCreateView.as_view()), #creating a feedback
    path('feedback/get-feedback/<int:feedback_id>/', FeedbackDetailView.as_view()), #getting a specific feedback
    path('feedback/<int:feedback_id>/delete-my-feedback/', DeleteFeedbackView.as_view()),# delete a specific feedback for a user logged in
    path('appointment/create-appointment/', AppointmentCreateView.as_view()),  # creating an appointment object
    path('appointment/all-appointments/', AppointmentListView.as_view()),  # get all appointments
    path('appointment/get-appointment/<int:appointment_id>/', AppointmentDetailView.as_view()),# get specific appointment based on the current logged in user
    path('appointment/<int:appointment_id>/delete-appointment/', AppointmentDeleteView.as_view()),# delete a specific appointment for a user logged in
    path('dog/all-dogs/', GetAllDogsView.as_view()),  # for getting all dogs from the database
    path('dog/my-dogs/', User_GetDogsView.as_view()),  # for getting all dogs of the currently logged in user
    path('dog/create-dog/', DogCreateView.as_view()),  # for creating a dog object
    path('dog/create-my-dog/', User_DogCreateView.as_view()),# for creating a dog object with onwer being currently logged in user
    path('dog/get-dog/<int:pk>', GetDogView.as_view()),  # for getting a dog object based on id
    path('dog/my-dog/<int:pk>', User_GetDogView.as_view()),# for getting currently logged-in user's dog based on id from query string
    path('dog/<int:pk>/delete-dog/', DogDeleteView.as_view()),  # for deleting the dog with id
    path('dog/<int:pk>/delete-my-dog/', User_DogDeleteView.as_view()),  # for updating dog's details from given id
    path('dog/<int:pk>/update-dog/', DogUpdateView.as_view()),  # for updating dog's details from given id
    path('dog/<int:pk>/update-my-dog/', User_DogUpdateView.as_view()),  # for updating dog's details from given id
    path('dog-feedback/all-dog-feedbacks/', GetAllDogsFeedBacksView.as_view()),# for getting all feedbacks of dogs from all dogwalkers
    path('dog-feedback/dog-feedbacks/<int:pk>', GetDogFeedbacksView.as_view()),# for getting all feedbacks of a single dog from diferent dogwalkers
    path('dog-feedback/create', CreateDogFeedbackView.as_view()),  # for creating dogfeedback
    path('dog-feedback/feedbacks-from-dogwalker', GetFeedbacksFromDogWalkerView.as_view()),# for getting all dogfeedbacks from a single dogwalker
]