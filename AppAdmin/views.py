from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializer import *
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from django.contrib.auth.models import User


class AddShopView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Shop.objects.all() 
    serializer_class = ShopOwnerSerializer
    
class ActionShopView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Shop.objects.all() 
    serializer_class = ShopOwnerSerializer
    
    
@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def ShopAdminUserView(request):
    if request.method == 'POST':
        serializer = ShopAdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        users = UserProfile.objects.filter(user__is_superuser=False, user__is_staff=True).select_related('user')
        serializer = UserProfileSerializer(users, many=True)
        return Response(serializer.data)
    
@api_view(['GET','PATCH'])    
@permission_classes([IsAdminUser])
def UpdateShopAdminUserView(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response('User Not Found', status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'PATCH':
        serializer = ShopAdminSerializer(user, data=request.data ,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        try:
            users = UserProfile.objects.get(user__id=id, user__is_superuser=False, user__is_staff=True)
        except UserProfile.DoesNotExist:
            return Response('User Profile Not Found', status=status.HTTP_400_BAD_REQUEST)
        serializer = UserProfileSerializer(users)
        return Response(serializer.data)
    