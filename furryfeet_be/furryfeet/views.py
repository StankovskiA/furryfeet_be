from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from rest_framework.exceptions import AuthenticationFailed
from .serializers import MyModelSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from .models import MyModel, User, Feedback, DogDetails

from datetime import datetime, timedelta
import jwt

class HelloWorld(APIView):
    def get(self, request):
        return Response({"message": "Hello World!"})
    
class MyModelList(generics.ListCreateAPIView):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer
    
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data)
    
class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed("User not found!")
        
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password!")

        payload = {
            'id': user.id,
            'exp': datetime.utcnow() + timedelta(minutes=120),
            'iat': datetime.utcnow()
        }
        
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            "jwt": token
        }
        
        return response

class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
            
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        
        return Response(serializer.data)
    
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        
        return response

class AddUserImageView(APIView):

    def post(self, request, pk):
        token = request.COOKIES.get('jwt')

        if not token:
          raise AuthenticationFailed("Unauthenticated!")
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            if payload['id'] == pk:
                user = User.objects.get(pk=pk)
            else:
                raise AuthenticationFailed("Unauthenticated!")
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found!")
        
        user.image = request.data.get('image')
        user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@login_required
def feedback(request, dog_id):
    # Get the dog details for the given id
    dog = get_object_or_404(DogDetails, dog_id=dog_id)

    if request.method == 'POST':
        # If the form was submitted, create a new feedback object
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        feedback = Feedback(rating=rating, comment=comment,
                            sender=request.user, receiver=dog.user)
        feedback.save()

    # Get all feedback objects for the given dog
    feedbacks = Feedback.objects.filter(receiver=dog.user)

    context = {
        'dog': dog,
        'feedbacks': feedbacks,
    }
    return render(request, 'feedback.html', context)

def dog_details(request, dog_id):
    # Get the dog details for the given id
    dog = get_object_or_404(DogDetails, dog_id=dog_id)

    context = {
        'dog': dog,
    }
    return render(request, 'dog_details.html', context)