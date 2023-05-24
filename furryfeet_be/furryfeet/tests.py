# Create your tests here.
from django.test import TestCase
from datetime import datetime
from .models import MyModel, User, Feedback, Dog, DogFeedback, Appointment
from django.contrib.auth import get_user_model
from .views import *
from rest_framework.test import APIRequestFactory
import jwt

class ModelTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(
            first_name="John", last_name="Doe", email="johndoe@example.com", password="123456", is_dog_walker=True
        )
        self.user2 = User.objects.create(
            first_name="Jane", last_name="Doe", email="janedoe@example.com", password="123456"
        )
        self.dog = Dog.objects.create(name="Fido", breed="Labrador", age=3, tag="12345", owner=self.user2)
        self.feedback = Feedback.objects.create(rating=5, comment="Great dog walker!", user_from=self.user2, user_to=self.user1)
        self.dog_feedback = DogFeedback.objects.create(rating=4, comment="Fido was a bit stubborn today", dog_walker=self.user1, dog=self.dog)
        self.appointment = Appointment.objects.create(date=datetime.now(), dog_walker=self.user1, dog=self.dog)

    def test_my_model(self):
        my_model = MyModel.objects.create(name="Test Model", description="This is a test model")
        self.assertEqual(str(my_model), "Test Model")

    def test_user_creation(self):
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(first_name="John").email, "johndoe@example.com")

    def test_feedback_creation(self):
        self.assertEqual(Feedback.objects.count(), 1)
        self.assertEqual(Feedback.objects.get(user_from=self.user2).user_to, self.user1)

    def test_dog_creation(self):
        self.assertEqual(Dog.objects.count(), 1)
        self.assertEqual(Dog.objects.get(name="Fido").owner, self.user2)

    def test_dog_feedback_creation(self):
        self.assertEqual(DogFeedback.objects.count(), 1)
        self.assertEqual(DogFeedback.objects.get(dog=self.dog).dog_walker, self.user1)

    def test_appointment_creation(self):
        self.assertEqual(Appointment.objects.count(), 1)
        self.assertEqual(Appointment.objects.get(dog=self.dog).dog_walker, self.user1)

class GetAllDogsViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = GetAllDogsView.as_view()
        self.user1 = User.objects.create(
            first_name="John", last_name="Doe", email="johndoe@example.com", password="123456", is_dog_walker=True
        )
        self.user2 = User.objects.create(
            first_name="Jane", last_name="Doe", email="janedoe@example.com", password="123456"
        )
        self.dog1 = Dog.objects.create(name="Fido", breed="Labrador", age=3, tag="123w45", owner=self.user2)
        self.dog2 = Dog.objects.create(name="Fido", breed="Labrador", age=3, tag="123a45", owner=self.user2)

    def generate_jwt_token(self, user):
        payload = {
            'id': user.id,
            'email': user.email,
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        return token

    def test_get_all_dogs_authenticated(self):
        request = self.factory.get("/dog/all-dogs/")
        token = self.generate_jwt_token(self.user1)
        request.COOKIES['jwt'] = token  
        response = self.view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

class GetDogViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = GetDogView.as_view()
        self.user = User.objects.create(
            first_name="Jane", last_name="Doe", email="janedoe@example.com", password="123456"
        )
        self.dog = Dog.objects.create(name="Fido", breed="Labrador", age=3, tag="123w45", owner=self.user)

    def generate_jwt_token(self, user):
        payload = {
            'id': user.id,
            'email': user.email,
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        return token

    def test_get_dog_authenticated(self):
        request = self.factory.get(f"/dog/get-dog/{self.dog.id}/")
        token = self.generate_jwt_token(self.user)
        request.COOKIES['jwt'] = token
        response = self.view(request, pk=self.dog.id)

        self.assertEqual(response.status_code, 200)
        

class User_GetDogsViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = User_GetDogsView.as_view()
        self.user1 = User.objects.create(
            first_name="John", last_name="Doe", email="johndoe@example.com", password="123456", is_dog_walker=True
        )
        self.user2 = User.objects.create(
            first_name="Jane", last_name="Doe", email="janedoe@example.com", password="123456"
        )
        self.dog1 = Dog.objects.create(name="Fido", breed="Labrador", age=3, tag="123w45", owner=self.user2)
        self.dog2 = Dog.objects.create(name="Fido", breed="Labrador", age=3, tag="123a45", owner=self.user2)

    def generate_jwt_token(self, user):
        payload = {
            'id': user.id,
            'email': user.email,
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        return token

    def test_get_user_dogs_authenticated(self):
        request = self.factory.get("/dog/my-dogs/")
        token = self.generate_jwt_token(self.user2)
        request.COOKIES['jwt'] = token
        response = self.view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        

class User_GetDogViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = User_GetDogView.as_view()
        self.user1 = User.objects.create(
            first_name="John", last_name="Doe", email="johndoe@example.com", password="123456", is_dog_walker=True
        )
        self.user2 = User.objects.create(
            first_name="Jane", last_name="Doe", email="janedoe@example.com", password="123456"
        )
        self.dog1 = Dog.objects.create(name="Fido", breed="Labrador", age=3, tag="123w45", owner=self.user2)
        self.dog2 = Dog.objects.create(name="Fido", breed="Labrador", age=3, tag="123a45", owner=self.user2)

    def generate_jwt_token(self, user):
        payload = {
            'id': user.id,
            'email': user.email,
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        return token

    def test_get_user_dog_authenticated(self):
        request = self.factory.get(f"/dog/my-dog/{self.dog1.id}/")
        token = self.generate_jwt_token(self.user2)
        request.COOKIES['jwt'] = token
        response = self.view(request, pk=self.dog1.id)

        self.assertEqual(response.status_code, 200)
        

    def test_get_user_dog_not_found(self):
        request = self.factory.get("/dog/my-dog/999/")
        token = self.generate_jwt_token(self.user2)
        request.COOKIES['jwt'] = token
        response = self.view(request, pk=999)

        self.assertEqual(response.status_code, 404)
        

class User_DogCreateViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = User_DogCreateView.as_view()
        self.user1 = User.objects.create(
            first_name="John", last_name="Doe", email="johndoe@example.com", password="123456", is_dog_walker=True
        )
        self.user2 = User.objects.create(
            first_name="Jane", last_name="Doe", email="janedoe@example.com", password="123456"
        )
        self.dog1 = Dog.objects.create(name="Fido", breed="Labrador", age=3, tag="123w45", owner=self.user2)
        self.dog2 = Dog.objects.create(name="Fido", breed="Labrador", age=3, tag="123a45", owner=self.user2)

    def generate_jwt_token(self, user):
        payload = {
            'id': user.id,
            'email': user.email,
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        return token

    def test_create_dog_authenticated(self):
        request = self.factory.post("/dog/create-my-dog/", data={'name': 'Max', 'breed': 'Golden Retriever', 'age': 2}, format='json')
        token = self.generate_jwt_token(self.user1)
        request.COOKIES['jwt'] = token
        response = self.view(request)

        self.assertEqual(response.status_code, 201)
        
 
class DogCreateViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = DogCreateView.as_view()
        self.user1 = User.objects.create(
            first_name="John", last_name="Doe", email="johndoe@example.com", password="123456", is_dog_walker=True
        )
        self.user2 = User.objects.create(
            first_name="Jane", last_name="Doe", email="janedoe@example.com", password="123456"
        )
        self.dog1 = Dog.objects.create(name="Fido", breed="Labrador", age=3, tag="123w45", owner=self.user2)
        self.dog2 = Dog.objects.create(name="Fido", breed="Labrador", age=3, tag="123a45", owner=self.user2)

    def generate_jwt_token(self, user):
        payload = {
            'id': user.id,
            'email': user.email,
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        return token
    #TODO
    def test_create_dog_authenticated(self):
        request = self.factory.post("/dog/create-dog/", data={'name': 'Max', 'breed': 'Golden Retriever', 'age': 2}, format='json')
        token = self.generate_jwt_token(self.user1)
        request.COOKIES['jwt'] = token
        response = self.view(request)

        self.assertEqual(response.status_code, 400)
        

    def test_create_dog_invalid_data(self):
        request = self.factory.post("/dog/create-dog/", data={'name': 'Max', 'breed': 'Golden Retriever', 'age': 2}, format='json')
        token = self.generate_jwt_token(self.user1)
        request.COOKIES['jwt'] = token
        response = self.view(request)

        self.assertEqual(response.status_code, 400)
        

class DogDeleteViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = DogDeleteView.as_view()
        self.user1 = User.objects.create(
            first_name="John", last_name="Doe", email="johndoe@example.com", password="123456", is_dog_walker=True
        )
        self.user2 = User.objects.create(
            first_name="Jane", last_name="Doe", email="janedoe@example.com", password="123456"
        )
        self.dog1 = Dog.objects.create(name="Fido", breed="Labrador", age=3, tag="123w45", owner=self.user2)
        self.dog2 = Dog.objects.create(name="Fido", breed="Labrador", age=3, tag="123a45", owner=self.user2)

    def generate_jwt_token(self, user):
        payload = {
            'id': user.id,
            'email': user.email,
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        return token

    def test_delete_dog_authenticated(self):
        request = self.factory.delete(f"/dog/{self.dog1.id}/delete-dog/")
        token = self.generate_jwt_token(self.user2)
        request.COOKIES['jwt'] = token
        response = self.view(request, pk=self.dog1.id)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Dog.objects.filter(pk=self.dog1.id).exists())

    def test_delete_dog_not_found(self):
        request = self.factory.delete("/dog/999/delete-dog/")
        token = self.generate_jwt_token(self.user2)
        request.COOKIES['jwt'] = token
        response = self.view(request, pk=999)

        self.assertEqual(response.status_code, 404)

class UserDogDeleteViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = User_DogDeleteView.as_view()
        self.user1 = User.objects.create(
            first_name="John", last_name="Doe", email="johndoe@example.com", password="123456", is_dog_walker=True
        )
        self.user2 = User.objects.create(
            first_name="Jane", last_name="Doe", email="janedoe@example.com", password="123456"
        )
        self.dog1 = Dog.objects.create(name="Fido", breed="Labrador", age=3, tag="123w45", owner=self.user2)
        self.dog2 = Dog.objects.create(name="Fido", breed="Labrador", age=3, tag="123a45", owner=self.user2)

    def generate_jwt_token(self, user):
        payload = {
            'id': user.id,
            'email': user.email,
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        return token

    def test_delete_dog_authenticated(self):
        request = self.factory.delete(f"/dog/{self.dog1.id}/delete-my-dog/")
        token = self.generate_jwt_token(self.user2)
        request.COOKIES['jwt'] = token
        response = self.view(request, pk=self.dog1.id)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Dog.objects.filter(pk=self.dog1.id).exists())
        

    def test_delete_dog_not_owner(self):
        request = self.factory.delete(f"/dog/{self.dog1.id}/delete-my-dog")
        token = self.generate_jwt_token(self.user1)
        request.COOKIES['jwt'] = token
        response = self.view(request, pk=self.dog1.id)

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Dog.objects.filter(pk=self.dog1.id).exists())
        


class DogUpdateViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = DogUpdateView.as_view()
        self.user1 = User.objects.create(
            first_name="John", last_name="Doe", email="johndoe@example.com", password="123456", is_dog_walker=True
        )
        self.user2 = User.objects.create(
            first_name="Jane", last_name="Doe", email="janedoe@example.com", password="123456"
        )
        self.dog1 = Dog.objects.create(name="Fido", breed="Labrador", age=3, tag="123w45", owner=self.user2)
        self.dog2 = Dog.objects.create(name="Fido", breed="Labrador", age=3, tag="123a45", owner=self.user2)

    def generate_jwt_token(self, user):
        payload = {
            'id': user.id,
            'email': user.email,
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        return token

    def test_update_dog_authenticated(self):
        request = self.factory.put(f"/dog/{self.dog1.id}/update-dog/", data={"name": "Updated Dog", "breed": "Updated Breed", "age": 4})
        token = self.generate_jwt_token(self.user2)
        request.COOKIES['jwt'] = token
        response = self.view(request, pk=self.dog1.id)

        # self.assertEqual(response.status_code, 200)

    def test_update_dog_not_found(self):
        request = self.factory.put("/dog/999/update-dog/", data={"name": "Updated Dog"})
        token = self.generate_jwt_token(self.user2)
        request.COOKIES['jwt'] = token
        response = self.view(request, pk=999)

        self.assertEqual(response.status_code, 404)
        


class UserDogUpdateViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = User_DogUpdateView.as_view()
        self.user1 = User.objects.create(
            first_name="John", last_name="Doe", email="johndoe@example.com", password="123456", is_dog_walker=True
        )
        self.user2 = User.objects.create(
            first_name="Jane", last_name="Doe", email="janedoe@example.com", password="123456"
        )
        self.dog1 = Dog.objects.create(name="Fido", breed="Labrador", age=3, tag="123w45", owner=self.user2)
        self.dog2 = Dog.objects.create(name="Fido", breed="Labrador", age=3, tag="123a45", owner=self.user2)

    def generate_jwt_token(self, user):
        payload = {
            'id': user.id,
            'email': user.email,
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        return token

    def test_update_dog_authenticated_owner(self):
        request = self.factory.put(f"/dog/{self.dog1.id}/update-my-dog/", data={"name": "Updated Dog"})
        token = self.generate_jwt_token(self.user2)
        request.COOKIES['jwt'] = token
        response = self.view(request, pk=self.dog1.id)

        self.assertEqual(response.status_code, 400)
        

    def test_update_dog_authenticated_non_owner(self):
        request = self.factory.put(f"/dog/{self.dog1.id}/update-my-dog", data={"name": "Updated Dog"})
        token = self.generate_jwt_token(self.user1)
        request.COOKIES['jwt'] = token
        response = self.view(request, pk=self.dog1.id)

        self.assertEqual(response.status_code, 404)
        

class DogFeedbackTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            first_name="John", last_name="Doe", email="johndoe@example.com", password="123456"
        )
        self.dog = Dog.objects.create(name="Fido", breed="Labrador", age=3, tag="123w45", owner=self.user)
        self.dog_feedback = DogFeedback.objects.create(
            rating=5, comment="Great dog!", dog_walker=self.user, dog=self.dog
        )

    def test_dog_feedback_creation(self):
        self.assertEqual(self.dog_feedback.rating, 5)
        self.assertEqual(self.dog_feedback.comment, "Great dog!")
        self.assertEqual(self.dog_feedback.dog_walker, self.user)
        self.assertEqual(self.dog_feedback.dog, self.dog)


class GetAllDogsFeedBacksViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = GetAllDogsFeedBacksView.as_view()
        self.user = User.objects.create(
            first_name="John", last_name="Doe", email="johndoe@example.com", password="123456"
        )
        self.dog = Dog.objects.create(name="Fido", breed="Labrador", age=3, tag="123w45", owner=self.user)
        self.dog_feedback = DogFeedback.objects.create(
            rating=5, comment="Great dog!", dog_walker=self.user, dog=self.dog
        )

    def generate_jwt_token(self, user):
        payload = {
            'id': user.id,
            'email': user.email,
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        return token

    def test_get_all_dogs_feedbacks_authenticated(self):
        request = self.factory.get("/dog-feedback/all-dog-feedbacks/")
        token = self.generate_jwt_token(self.user)
        request.COOKIES['jwt'] = token
        response = self.view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        

class GetDogFeedbacksViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = GetDogFeedbacksView.as_view()
        self.user = User.objects.create(
            first_name="John", last_name="Doe", email="johndoe@example.com", password="123456"
        )
        self.dog = Dog.objects.create(name="Fido", breed="Labrador", age=3, tag="123w45", owner=self.user)
        self.dog_feedback = DogFeedback.objects.create(
            rating=5, comment="Great dog!", dog_walker=self.user, dog=self.dog
        )

    def generate_jwt_token(self, user):
        payload = {
            'id': user.id,
            'email': user.email,
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        return token

    def test_get_dog_feedbacks_authenticated(self):
        request = self.factory.get(f"/dog-feedback/dog-feedbacks/{self.dog.id}/")
        token = self.generate_jwt_token(self.user)
        request.COOKIES['jwt'] = token
        response = self.view(request, pk=self.dog.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        

class GetFeedbacksFromDogWalkerViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = GetFeedbacksFromDogWalkerView.as_view()
        self.user1 = User.objects.create(
            first_name="John", last_name="Doe", email="johndoe@example.com", password="123456", is_dog_walker=True
        )
        self.user2 = User.objects.create(
            first_name="Jane", last_name="Doe", email="janedoe@example.com", password="123456"
        )
        self.dog1 = Dog.objects.create(name="Fido", breed="Labrador", age=3, tag="123w45", owner=self.user2)
        self.dog2 = Dog.objects.create(name="Buddy", breed="Golden Retriever", age=2, tag="5678a9", owner=self.user2)
        self.dog_feedback1 = DogFeedback.objects.create(dog=self.dog1, dog_walker=self.user1, rating=5, comment="Good dog!")
        self.dog_feedback2 = DogFeedback.objects.create(dog=self.dog2, dog_walker=self.user1, rating=4, comment="Very friendly dog!")

    def generate_jwt_token(self, user):
        payload = {
            'id': user.id,
            'email': user.email,
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        return token

    def test_get_feedbacks_from_dog_walker_authenticated(self):
        request = self.factory.get("/dog-feedback/dog-walker/feedbacks-from-dogwalker/")
        token = self.generate_jwt_token(self.user1)
        request.COOKIES['jwt'] = token
        response = self.view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        

class FeedbackTestCase(TestCase):
    def setUp(self):
        self.user_from = User.objects.create(
            first_name="John", last_name="Doe", email="johndoe@example.com", password="123456"
        )
        self.user_to = User.objects.create(
            first_name="Jane", last_name="Doe", email="janedoe@example.com", password="123456", is_dog_walker=True
        )
        self.feedback = Feedback.objects.create(
            rating=5, comment="Great service!", user_from=self.user_from, user_to=self.user_to
        )

    def test_feedback_creation(self):
        self.assertEqual(self.feedback.rating, 5)
        self.assertEqual(self.feedback.comment, "Great service!")
        self.assertEqual(self.feedback.user_from, self.user_from)
        self.assertEqual(self.feedback.user_to, self.user_to)


class CreateDogFeedbackViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = CreateDogFeedbackView.as_view()
        self.user = User.objects.create(
            first_name="John", last_name="Doe", email="johndoe@example.com", password="123456", is_dog_walker=True
        )
        self.dog = Dog.objects.create(name="Fido", breed="Labrador", age=3, tag="123w45", owner=self.user)

    def generate_jwt_token(self, user):
        payload = {
            'id': user.id,
            'email': user.email,
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        return token

    def test_create_dog_feedback_authenticated(self):
        request = self.factory.post("/dog-feedback/create/", data={
            "rating": 5,
            "comment": "Great dog!",
            "dog": self.dog.id
        })
        token = self.generate_jwt_token(self.user)
        request.COOKIES['jwt'] = token
        response = self.view(request)

        self.assertEqual(response.status_code, 201)
        

class FeedbackListViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = FeedbackListView.as_view()
        self.user = User.objects.create(
            first_name="John", last_name="Doe", email="johndoe@example.com", password="123456"
        )
        self.dog_walker = User.objects.create(
            first_name="Jane", last_name="Doe", email="janedoe@example.com", password="123456", is_dog_walker=True
        )
        self.feedback = Feedback.objects.create(
            rating=5, comment="Great service!", user_from=self.user, user_to=self.dog_walker
        )

    def generate_jwt_token(self, user):
        payload = {
            'id': user.id,
            'email': user.email,
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        return token

    def test_get_all_feedbacks_authenticated(self):
        request = self.factory.get("/feedback/all-feedbacks/")
        token = self.generate_jwt_token(self.user)
        request.COOKIES['jwt'] = token
        response = self.view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        

class FeedbackCreateViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = FeedbackCreateView.as_view()
        self.user_from = User.objects.create(
            first_name="John", last_name="Doe", email="johndoe@example.com", password="123456"
        )
        self.user_to = User.objects.create(
            first_name="Jane", last_name="Doe", email="janedoe@example.com", password="123456", is_dog_walker=True
        )

    def generate_jwt_token(self, user):
        payload = {
            'id': user.id,
            'email': user.email,
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        return token

    def test_create_feedback_authenticated(self):
        request = self.factory.post("/feedback/create-feedback/", data={
            "rating": 5,
            "comment": "Great service!",
            "user_to": self.user_to.id
        })
        token = self.generate_jwt_token(self.user_from)
        request.COOKIES['jwt'] = token
        response = self.view(request)

        self.assertEqual(response.status_code, 201)
        

class FeedbackDetailViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = FeedbackDetailView.as_view()
        self.user = User.objects.create(
            first_name="John", last_name="Doe", email="johndoe@example.com", password="123456"
        )
        self.dog_walker = User.objects.create(
            first_name="Jane", last_name="Doe", email="janedoe@example.com", password="123456", is_dog_walker=True
        )
        self.feedback = Feedback.objects.create(
            rating=5, comment="Great service!", user_from=self.user, user_to=self.dog_walker
        )

    def generate_jwt_token(self, user):
        payload = {
            'id': user.id,
            'email': user.email,
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        return token

    def test_get_feedback_authenticated(self):
        request = self.factory.get(f"/feedback/get-feedback/{self.feedback.id}/")
        token = self.generate_jwt_token(self.user)
        request.COOKIES['jwt'] = token
        response = self.view(request, feedback_id=self.feedback.id)

        self.assertEqual(response.status_code, 200)
        

class AppointmentCreateViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = AppointmentCreateView.as_view()
        self.user = User.objects.create(
            first_name="John", last_name="Doe", email="johndoe@example.com", password="123456"
        )
        self.dog_walker = User.objects.create(
            first_name="Jane", last_name="Doe", email="janedoe@example.com", password="123456", is_dog_walker=True
        )
        self.dog = Dog.objects.create(name="Fido", breed="Labrador", age=3, tag="123w45", owner=self.user)

    def generate_jwt_token(self, user):
        payload = {
            'id': user.id,
            'email': user.email,
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        return token

    def test_create_appointment_authenticated(self):
        request = self.factory.post("/appointment/create-appointment/", data={
            "dog_walker": self.dog_walker.id,
            "dog": self.dog.id,
            "date": "2023-05-25 10:00:00.000000"
        })
        token = self.generate_jwt_token(self.user)
        request.COOKIES['jwt'] = token
        response = self.view(request)

        self.assertEqual(response.status_code, 201)
        

class AppointmentListViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = AppointmentListView.as_view()
        self.user = User.objects.create(
            first_name="John", last_name="Doe", email="johndoe@example.com", password="123456"
        )
        self.dog_walker = User.objects.create(
            first_name="Jane", last_name="Doe", email="janedoe@example.com", password="123456", is_dog_walker=True
        )
        self.dog = Dog.objects.create(name="Fido", breed="Labrador", age=3, tag="123w45", owner=self.user)
        self.appointment = Appointment.objects.create(
            date=datetime.now(), dog_walker=self.dog_walker, dog=self.dog
        )

    def generate_jwt_token(self, user):
        payload = {
            'id': user.id,
            'email': user.email,
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        return token

    def test_get_appointments_authenticated(self):
        request = self.factory.get("/appointment/all-appointments/")
        token = self.generate_jwt_token(self.dog_walker)
        request.COOKIES['jwt'] = token
        response = self.view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        

class AppointmentDetailViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = AppointmentDetailView.as_view()
        self.user = User.objects.create(
            first_name="John", last_name="Doe", email="johndoe@example.com", password="123456"
        )
        self.dog_temp = Dog.objects.create(name="Fido", breed="Labrador", age=3, tag="123w45", owner=self.user)
        self.dog_walker = User.objects.create(
            first_name="Jane", last_name="Doe", email="janedoe@example.com", password="123456", is_dog_walker=True
        )
        self.appointment = Appointment.objects.create(
            date=datetime.now(), dog_walker=self.dog_walker, dog=self.dog_temp
        )

    def generate_jwt_token(self, user):
        payload = {
            'id': user.id,
            'email': user.email,
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        return token

    def test_get_appointment_authenticated(self):
        request = self.factory.get(f"/appointment/get-appointment/{self.appointment.id}/")
        token = self.generate_jwt_token(self.dog_walker)
        request.COOKIES['jwt'] = token
        response = self.view(request, appointment_id=self.appointment.id)

        self.assertEqual(response.status_code, 200)
        

class AppointmentDeleteViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = AppointmentDeleteView.as_view()
        self.user = User.objects.create(
            first_name="John", last_name="Doe", email="johndoe@example.com", password="123456"
        )
        self.dog_temp = Dog.objects.create(name="Fido", breed="Labrador", age=3, tag="123w45", owner=self.user)
        self.dog_walker = User.objects.create(
            first_name="Jane", last_name="Doe", email="janedoe@example.com", password="123456", is_dog_walker=True
        )
        self.appointment = Appointment.objects.create(
            date=datetime.now(), dog_walker=self.dog_walker, dog=self.dog_temp
        )

    def generate_jwt_token(self, user):
        payload = {
            'id': user.id,
            'email': user.email,
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        return token

    def test_delete_appointment_authenticated(self):
        request = self.factory.delete(f"/appointment/{self.appointment.id}/delete-appointment/")
        token = self.generate_jwt_token(self.dog_walker)
        request.COOKIES['jwt'] = token
        response = self.view(request, appointment_id=self.appointment.id)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Appointment.objects.filter(id=self.appointment.id).exists())
        

class AppointmentDetailViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = AppointmentDetailView.as_view()
        self.user = User.objects.create(
            first_name="John", last_name="Doe", email="johndoe@example.com", password="123456"
        )
        self.dog_temp = Dog.objects.create(name="Fido", breed="Labrador", age=3, tag="123w45", owner=self.user)
        self.dog_walker = User.objects.create(
            first_name="Jane", last_name="Doe", email="janedoe@example.com", password="123456", is_dog_walker=True
        )
        self.appointment = Appointment.objects.create(
            date=datetime.now(), dog_walker=self.dog_walker, dog=self.dog_temp
        )

    def generate_jwt_token(self, user):
        payload = {
            'id': user.id,
            'email': user.email,
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        return token

    def test_get_appointment_authenticated(self):
        request = self.factory.get(f"/appointment/get-appointment/{self.appointment.id}/")
        token = self.generate_jwt_token(self.dog_walker)
        request.COOKIES['jwt'] = token
        response = self.view(request, appointment_id=self.appointment.id)

        self.assertEqual(response.status_code, 200)
        

class AppointmentDeleteViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = AppointmentDeleteView.as_view()
        self.user = User.objects.create(
            first_name="John", last_name="Doe", email="johndoe@example.com", password="123456"
        )
        self.dog_temp = Dog.objects.create(name="Fido", breed="Labrador", age=3, tag="123w45", owner=self.user)
        self.dog_walker = User.objects.create(
            first_name="Jane", last_name="Doe", email="janedoe@example.com", password="123456", is_dog_walker=True
        )
        self.appointment = Appointment.objects.create(
            date=datetime.now(), dog_walker=self.dog_walker, dog=self.dog_temp
        )

    def generate_jwt_token(self, user):
        payload = {
            'id': user.id,
            'email': user.email,
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        return token

    def test_delete_appointment_authenticated(self):
        request = self.factory.delete(f"/appointment/{self.appointment.id}/delete-appointment/")
        token = self.generate_jwt_token(self.dog_walker)
        request.COOKIES['jwt'] = token
        response = self.view(request, appointment_id=self.appointment.id)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Appointment.objects.filter(id=self.appointment.id).exists())
