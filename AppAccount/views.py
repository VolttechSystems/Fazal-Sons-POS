from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from .serializer import *
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view
from rest_framework.decorators import api_view

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
        token, _ = Token.objects.get_or_create(user=user_obj)
        if user_obj:
            return Response({
                "status": True,
                "data": {"token": str(token)}
            })

        return Response({
            "status": False,
            "data": {},
            "Message": "Invalid Credential"
        })


class LogoutView(APIView):
    def post(self, request):
        request.user.auth_token.delete()  # Delete the user's authentication token
        return Response({"message": "Successfully logged out."})


class CreateUserView(generics.ListCreateAPIView):
    model = get_user_model()
    # authentication_classes = [SessionAuthentication]
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
@api_view(["GET"])
def FazalSons(request):
    return Response("Backend in Working Fine")
    
    
@api_view(["GET"])
def FazalSons(request):
    return Response("Backend in Working Fine")
