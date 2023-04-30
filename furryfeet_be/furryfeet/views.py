from rest_framework.exceptions import AuthenticationFailed
from .serializers import MyModelSerializer, UserSerializer, AppointmentSerializer, FeedbackSerializer, DogWalkerSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from .models import MyModel, User, Appointment, DogWalker, Feedback

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
    

class DogWalkerView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
          raise AuthenticationFailed("Unauthenticated!")
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
         
        try:
            dog_walker = DogWalker.objects.get(user=request.user)
            serializer = DogWalkerSerializer(dog_walker)
            appointments = dog_walker.appointments.all()
            feedbacks = dog_walker.feedbacks.all()
            return Response({'dog_walker': serializer.data, 'appointments': AppointmentSerializer(appointments, many=True).data, 'feedbacks': FeedbackSerializer(feedbacks, many=True).data})
        except DogWalker.DoesNotExist:
            return Response(status=404)

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

        serializer = DogWalkerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request, pk):
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

        try:
            dog_walker = DogWalker.objects.get(user=request.user)
            serializer = DogWalkerSerializer(dog_walker, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except DogWalker.DoesNotExist:
            return Response(status=404)


class AppointmentView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
          raise AuthenticationFailed("Unauthenticated!")
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
        appointments = Appointment.objects.filter(dogWalker__user=request.user)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

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
        
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(dogOwner=request.user, dogWalker=DogWalker.objects.get(user=request.data['dogWalker']))
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class FeedbackView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
          raise AuthenticationFailed("Unauthenticated!")
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        feedbacks = Feedback.objects.filter(dogWalker__user=request.user)
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data)

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
        
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(dogOwner=request.user, dogWalker=DogWalker.objects.get(user=request.data['dogWalker']))
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)