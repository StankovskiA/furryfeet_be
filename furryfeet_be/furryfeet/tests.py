# Create your tests here.
from django.test import TestCase
from datetime import datetime
from .models import MyModel, User, Feedback, Dog, DogFeedback, Appointment

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
