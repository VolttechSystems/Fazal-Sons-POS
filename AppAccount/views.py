from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework import status

from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view
from rest_framework.decorators import api_view

##### Automatically create a profile for new users
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import *
from .serializer import *

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


## Login View 
class LoginAPIView(APIView):

    def post(self, request):
        data = request.data
        serializer = LoginSerializers(data=data)
        if not serializer.is_valid():
            return Response({
                "status": False,
                "data": serializer.data
            })
        username = serializer.data['username']
        password = serializer.data['password']

        user_obj = authenticate(username=username, password=password)
        if user_obj is None:
            return Response({"error": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)
        
        if user_obj.is_active:
            token, created = Token.objects.get_or_create(user=user_obj)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User is inactive"}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            # Delete token if authenticated
            request.user.auth_token.delete()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        else:
            # Handle unauthenticated users
            return Response({"detail": "User is not authenticated."}, status=status.HTTP_200_OK)

class CreateUserView(generics.ListCreateAPIView):
    model = get_user_model()
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
### For Api Test 
@api_view(["GET"])
def FazalSons(request):
    return Response("Backend in Working Fine")
    
