from rest_framework import serializers
from .models import MyModel, User, DogWalker, Feedback, Appointment

class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'image']
        extra_kwargs = {
            'password': {'write_only': True}    
        }
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        
        if password is not None:
            instance.set_password(password)
        instance.save()
        
        return instance



class DogWalkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DogWalker
        fields = ['id']


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['date']


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '_all_'