from rest_framework.exceptions import AuthenticationFailed
from .serializers import MyModelSerializer, UserSerializer, DogSerializer, DogFeedbackSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from .models import MyModel, User, Dog, DogFeedback

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

# This view is used for getting all dogs from the database
class GetAllDogsView(APIView):
    def get(self, request):
        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("Unauthenticated!")
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
        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("Unauthenticated!")
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
        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("Unauthenticated!")
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
        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("Unauthenticated!")
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
        token = request.COOKIES.get("jwt")

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
        token = request.COOKIES.get("jwt")

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
        token = request.COOKIES.get("jwt")

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
        token = request.COOKIES.get("jwt")

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
        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            dog = Dog.objects.get(pk=pk)
        except Dog.DoesNotExist:
            return Response(
                {"message": "Dog not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = DogSerializer(dog, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# This view is used for updating a dog only if the currently logged in user is his/her owner
class User_DogUpdateView(APIView):
    def put(self, request, pk):
        token = request.COOKIES.get("jwt")

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
        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("Unauthenticated!")
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
        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("Unauthenticated!")
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
        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("Unauthenticated!")
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
        token = request.COOKIES.get("jwt")

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