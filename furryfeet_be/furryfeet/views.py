from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from .methods import is_password_valid
from .serializers import *
from .models import *

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
        token_header = request.headers.get('Authorization')
        token_cookie = request.COOKIES.get('jwt')
        
        token = token_header if token_header is not None else token_cookie
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        
        token = token.split(' ')[1] if token.startswith('Bearer ') else token
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
            
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        
        return Response(serializer.data)
    
class GetAllDogWallkers(APIView):
    def get(self, request):
        token_header = request.headers.get('Authorization')
        token_cookie = request.COOKIES.get('jwt')
        token = token_header if token_header is not None else token_cookie
        
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        
        token = token.split(' ')[1] if token.startswith('Bearer ') else token
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
        dog_walkers = User.objects.filter(is_dog_walker=True)

        serializer = UserSerializer(dog_walkers, many=True)
        return Response(serializer.data)
    
class GetDogWallkerById(APIView):
    def get(self, request, id):
        token_header = request.headers.get('Authorization')
        token_cookie = request.COOKIES.get('jwt')
        token = token_header if token_header is not None else token_cookie

        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        
        token = token.split(' ')[1] if token.startswith('Bearer ') else token
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            dog_walker = User.objects.get(id=id, is_dog_walker=True)
        except User.DoesNotExist:
            return Response({"error": "Dog walker not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(dog_walker)
        return Response(serializer.data)
    
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        
        return response

class ChangeUserPasswordView(APIView):
    def post(self, request):
        token_data = request.data['jwt']
        token_cookie = request.COOKIES.get('jwt')
        
        token = token_data if token_data is not None else token_cookie
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
        user = User.objects.get(id=payload['id'])
        current_password = request.data["current_password"]
        new_password1 = request.data["new_password1"]
        new_password2 = request.data["new_password2"]
        
        # Verify the current password
        if not user.check_password(current_password):
            
            return Response({"error": "Incorrect current password"}, status=400)
        
        # Verify that the new passwords match
        if new_password1 != new_password2:
            return Response({"error": "New passwords do not match"}, status=400)
        
        # Verify that the new password meets the policy requirements
        if not is_password_valid(new_password1):
            return Response({"error": "New password does not meet the policy requirements"}, status=400)
        
        # Change the user's password and update the session
        user.set_password(new_password1)
        user.save()
        update_session_auth_hash(request, user)
        
        return Response({"message": "Password successfully changed"})

class AddUserImageView(APIView):

    def post(self, request, pk):
        token_data = request.data['jwt']
        token_cookie = request.COOKIES.get('jwt')
        
        token = token_data if token_data is not None else token_cookie
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

# This view is used for getting all dogs from the database
class GetAllDogsView(APIView):
    def get(self, request):
        token_header = request.headers.get('Authorization')
        token_cookie = request.COOKIES.get('jwt')
        
        token = token_header if token_header is not None else token_cookie
        if not token:
            raise AuthenticationFailed("Unauthenticated!")        
        
        token = token.split(' ')[1] if token.startswith('Bearer ') else token
        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            dogs = Dog.objects.all()
            serializer = DogSerializer(dogs, many=True)
            return Response(serializer.data)
        except Dog.DoesNotExist:
            return Response(
                {"message": "No dogs found"}, status=status.HTTP_404_NOT_FOUND
            )


# This view is used for getting single dog object based on id from query string
class GetDogView(APIView):
    def get(self, request, pk):
        token_header = request.headers.get('Authorization')
        token_cookie = request.COOKIES.get('jwt')
        
        token = token_header if token_header is not None else token_cookie
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        
        token = token.split(' ')[1] if token.startswith('Bearer ') else token
        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            dog = Dog.objects.get(id=pk)
        except Dog.DoesNotExist:
            message = f"Dog with id {pk} is not found"
            return Response({"message": message}, status=status.HTTP_404_NOT_FOUND)

        serialized_dog = DogSerializer(dog)

        return Response(serialized_dog.data)


# This view is used for getting currently logged in user's all dogs
class User_GetDogsView(APIView):
    def get(self, request):
        token_header = request.headers.get('Authorization')
        token_cookie = request.COOKIES.get('jwt')
        
        token = token_header if token_header is not None else token_cookie
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        
        token = token.split(' ')[1] if token.startswith('Bearer ') else token
        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            dogs = Dog.objects.filter(owner_id=payload["id"])
            serialized_dog = DogSerializer(dogs, many=True)
            return Response(serialized_dog.data)

        except Dog.DoesNotExist:
            user = User.objects.get(id=payload["id"])
            message = f"User with id [{payload['id']}] with email address [{user.email}] does not have any dogs registered"
            return Response({"message": message}, status=status.HTTP_404_NOT_FOUND)


# This view is used for getting currently logged-in user's dog based on id from query string
class User_GetDogView(APIView):
    def get(self, request, pk):
        token_header = request.headers.get('Authorization')
        token_cookie = request.COOKIES.get('jwt')
        
        token = token_header if token_header is not None else token_cookie
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        
        token = token.split(' ')[1] if token.startswith('Bearer ') else token
        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            my_dog = Dog.objects.get(id=pk, owner_id=payload["id"])
        except Dog.DoesNotExist:
            user = User.objects.get(id=payload["id"])
            message = f"User with ID {payload['id']} with email address [{user.email}] does not have a dog with ID {pk}"
            return Response({"message": message}, status=status.HTTP_404_NOT_FOUND)

        serialized_dog = DogSerializer(my_dog)

        return Response(serialized_dog.data)

# this view is used for creating dog object with owner being currently logged-in user
class User_DogCreateView(APIView):
    def post(self, request):
        token_data = request.data['jwt']
        token_cookie = request.COOKIES.get('jwt')
        
        token = token_data if token_data is not None else token_cookie
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        
        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        dogOwner = User.objects.get(id=payload["id"])
        serializered_dog = DogSerializer(data=request.data, partial=True)
        if serializered_dog.is_valid():
            serializered_dog.save(owner=dogOwner)
            return Response(serializered_dog.data, status=201)
        return Response(serializered_dog.errors, status=400)


# this view is used for creating dog object
class DogCreateView(APIView):
    def post(self, request):
        token_data = request.data['jwt']
        token_cookie = request.COOKIES.get('jwt')
        
        token = token_data if token_data is not None else token_cookie
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        
        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
        serializered_dog = DogSerializer(data=request.data)
        if serializered_dog.is_valid():
            serializered_dog.save()
            return Response(serializered_dog.data, status=201)
        return Response(serializered_dog.errors, status=400)



# This view is used for deleting the dog from the database with given id
class DogDeleteView(APIView):
    def delete(self, request, pk):
        token_data = request.data['jwt']
        token_cookie = request.COOKIES.get('jwt')
        
        token = token_data if token_data is not None else token_cookie
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        
        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            dog = Dog.objects.get(pk=pk)
            dog.delete()
            return Response(
                {"message": "Dog deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Dog.DoesNotExist:
            return Response(
                {"message": "Dog not found"}, status=status.HTTP_404_NOT_FOUND
            )


# This view is used for deleting a dog only if the currently logged in user is his/her owner
class User_DogDeleteView(APIView):
    def delete(self, request, pk):
        token_data = request.data['jwt']
        token_cookie = request.COOKIES.get('jwt')
        
        token = token_data if token_data is not None else token_cookie
        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            dog = Dog.objects.get(pk=pk, owner_id=payload["id"])
        except Dog.DoesNotExist:
            return Response(
                {"message": "DELETING NOT ALLOWED! You are not the owner of this dog"},
                status=status.HTTP_404_NOT_FOUND,
            )

        dog.delete()
        return Response(
            {"message": "Dog deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )


# This view is used for updating dog's details
class DogUpdateView(APIView):
    def put(self, request, pk):
        token_data = request.data['jwt']
        token_cookie = request.COOKIES.get('jwt')
        
        token = token_data if token_data is not None else token_cookie
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        
        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            dog = Dog.objects.get(pk=pk)
        except Dog.DoesNotExist:
            return Response({"message": "Dog not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DogSerializer(dog, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# This view is used for updating a dog only if the currently logged in user is his/her owner
class User_DogUpdateView(APIView):
    def put(self, request, pk):
        token_data = request.data['jwt']
        token_cookie = request.COOKIES.get('jwt')
        
        token = token_data if token_data is not None else token_cookie
        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            dog = Dog.objects.get(pk=pk, owner_id=payload["id"])
        except Dog.DoesNotExist:
            return Response(
                {"message": "UPDATING NOT ALLOWED! You are not the owner of this dog"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = DogSerializer(dog, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# This view is used for getting all dog feedbacks from all different dog walkers
class GetAllDogsFeedBacksView(APIView):
    def get(self, request):
        token_header = request.headers.get('Authorization')
        token_cookie = request.COOKIES.get('jwt')
        
        token = token_header if token_header is not None else token_cookie
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        
        token = token.split(' ')[1] if token.startswith('Bearer ') else token
        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            dogs_Feedbacks = DogFeedback.objects.all()
            serializer = DogFeedbackSerializer(dogs_Feedbacks, many=True)
            return Response(serializer.data)
        except Dog.DoesNotExist:
            return Response(
                {"message": "No dogs found"}, status=status.HTTP_404_NOT_FOUND
            )


# This view is used for getting single dog's all feedbacks recieved from different dogwalkers
class GetDogFeedbacksView(APIView):
    def get(self, request, pk):
        token_header = request.headers.get('Authorization')
        token_cookie = request.COOKIES.get('jwt')
        
        token = token_header if token_header is not None else token_cookie
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        
        token = token.split(' ')[1] if token.startswith('Bearer ') else token
        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            dog_feedbacks = DogFeedback.objects.filter(dog=pk)
        except DogFeedback.DoesNotExist:
            message = f"DogFeedbacks not found"
            return Response({"message": message}, status=status.HTTP_404_NOT_FOUND)

        serialized_dog = DogFeedbackSerializer(dog_feedbacks, many=True)

        return Response(serialized_dog.data)


# This view is used for getting all feedbackts given to the dogs from a DogWalker
class GetFeedbacksFromDogWalkerView(APIView):
    def get(self, request):
        token_header = request.headers.get('Authorization')
        token_cookie = request.COOKIES.get('jwt')
        
        token = token_header if token_header is not None else token_cookie
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        
        token = token.split(' ')[1] if token.startswith('Bearer ') else token
        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            dog_feedbacks_DW = DogFeedback.objects.filter(dog_walker=payload["id"])
        except Dog.DoesNotExist:
            message = f"DogFeedbacks not found"
            return Response({"message": message}, status=status.HTTP_404_NOT_FOUND)

        serialized_dog = DogFeedbackSerializer(dog_feedbacks_DW, many=True)

        return Response(serialized_dog.data)


# This view is used to create a feedback for a dog if the currently logged in user is dogwalker (is_dog_walker=True)
class CreateDogFeedbackView(APIView):
    def post(self, request):
        token_data = request.data['jwt']
        token_cookie = request.COOKIES.get('jwt')
        
        token = token_data if token_data is not None else token_cookie

        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        user = User.objects.get(id=payload["id"])
        if not user.is_dog_walker:
            return Response(
                {"error": "Current user is not a dog walker."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = DogFeedbackSerializer(data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save(dog_walker=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#FeedbackListView
class FeedbackListView(APIView):
    def get(self, request):
        token_header = request.headers.get('Authorization')
        token_cookie = request.COOKIES.get('jwt')
        
        token = token_header if token_header is not None else token_cookie
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        
        token = token.split(' ')[1] if token.startswith('Bearer ') else token
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        feedbacks = Feedback.objects.all()
        serializer = FeedbackSerializer(feedbacks, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class FeedbackCreateView(APIView):
    def post(self, request):
        token_data = request.data['jwt']
        token_cookie = request.COOKIES.get('jwt')
        
        token = token_data if token_data is not None else token_cookie
        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        # get the user who is posting the feedback
        user_from = User.objects.get(id=payload['id'])

        # get the user who is receiving the feedback
        user_to_id = request.data.get('user_to')
        user_to = User.objects.get(id=user_to_id)

        # create the feedback object
        feedback = Feedback(
            rating=request.data.get('rating'),
            comment=request.data.get('comment'),
            user_from=user_from,
            user_to=user_to
        )
        feedback.save()

        serializer = FeedbackSerializer(feedback)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class FeedbackDetailView(APIView):
    def get(self, request, feedback_id):
        token_header = request.headers.get('Authorization')
        token_cookie = request.COOKIES.get('jwt')
        
        token = token_header if token_header is not None else token_cookie
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        
        token = token.split(' ')[1] if token.startswith('Bearer ') else token
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        feedback = Feedback.objects.get(pk=feedback_id)
        serializer = FeedbackSerializer(feedback)

        return Response(serializer.data, status=status.HTTP_200_OK)

class AppointmentCreateView(APIView):
    def post(self, request):
        iso_format = '%Y-%m-%d %H:%M:%S.%f'
        token_data = request.data['jwt']
        token_cookie = request.COOKIES.get('jwt')
        
        token = token_data if token_data is not None else token_cookie
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        # get the dog walker id from request data
        dog_walker_id = request.data.get('dog_walker')

        # check if the user is a dog walker
        try:
            dog_walker = User.objects.get(id=dog_walker_id, is_dog_walker=True)
        except User.DoesNotExist:
            return Response({'error': 'Invalid dog walker ID or user is not a dog walker.'}, status=status.HTTP_400_BAD_REQUEST)

        # get the dog id from request data
        dog_id = request.data.get('dog')

        # check if the dog exists
        try:
            dog = Dog.objects.get(id=dog_id)
        except Dog.DoesNotExist:
            return Response({'error': 'Invalid dog ID.'}, status=status.HTTP_400_BAD_REQUEST)

        # get the appointment date from request data
        date_str = request.data.get('date')
        try:
            date = datetime.strptime(date_str, iso_format)
        except ValueError:
            return Response({'error': 'Invalid date format. Please use ISO format.'}, status=status.HTTP_400_BAD_REQUEST)

        # create the appointment object
        appointment = Appointment.objects.create(
            dog_walker=dog_walker,
            dog=dog,
            date=date,
        )

        # serialize the appointment object and return the response
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class AppointmentListView(APIView):
    def get(self, request):
        token_header = request.headers.get('Authorization')
        token_cookie = request.COOKIES.get('jwt')
        
        token = token_header if token_header is not None else token_cookie
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        
        token = token.split(' ')[1] if token.startswith('Bearer ') else token
        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        user = User.objects.get(id=payload["id"])

        if not user.is_dog_walker:
            return Response({"error": "Current user is not a dog walker."}, status=status.HTTP_403_FORBIDDEN)

        appointments = Appointment.objects.filter(dog_walker=user).all()
        serializer = AppointmentSerializer(appointments, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class AppointmentDetailView(APIView):
    def get(self, request, appointment_id):
        token_header = request.headers.get('Authorization')
        token_cookie = request.COOKIES.get('jwt')
        
        token = token_header if token_header is not None else token_cookie
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        token = token.split(' ')[1] if token.startswith('Bearer ') else token
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return Response({'error': 'Invalid appointment ID.'}, status=status.HTTP_400_BAD_REQUEST)

        if appointment.dog_walker.id != payload['id']:
            return Response({'error': 'Unauthorized to view this appointment.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AppointmentDeleteView(APIView):
    def delete(self, request, appointment_id):
        token_data = request.data['jwt']
        token_cookie = request.COOKIES.get('jwt')
        
        token = token_data if token_data is not None else token_cookie
        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        appointment = get_object_or_404(Appointment, pk=appointment_id)

        # Only allow the dog walker who created the appointment to delete it
        if appointment.dog_walker.id != payload['id']:
            return Response({'error': 'You do not have permission to delete this appointment'},
                            status=status.HTTP_403_FORBIDDEN)

        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeleteFeedbackView(APIView):
    def delete(self, request, feedback_id):
        token_data = request.data['jwt']
        token_cookie = request.COOKIES.get('jwt')
        
        token = token_data if token_data is not None else token_cookie
        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        user = User.objects.get(id=payload["id"])
        try:
            feedback = Feedback.objects.get(id=feedback_id)
        except Feedback.DoesNotExist:
            return Response({"error": "Invalid feedback ID."}, status=status.HTTP_400_BAD_REQUEST)

        if not user.is_dog_walker and feedback.dog_owner != user:
            return Response(
                {"error": "Current user is not authorized to delete this feedback."},
                status=status.HTTP_403_FORBIDDEN,
            )

        feedback.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)