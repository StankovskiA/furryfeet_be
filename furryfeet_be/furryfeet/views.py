from rest_framework.response import Response
from .serializers import MyModelSerializer
from rest_framework.views import APIView
from rest_framework import generics
from .models import MyModel

# Create your views here.
class HelloWorld(APIView):
    def get(self, request):
        return Response({"message": "Hello World!"})
    
class MyModelList(generics.ListCreateAPIView):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer