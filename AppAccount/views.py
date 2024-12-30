# from rest_framework.authtoken.models import Token
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from django.contrib.auth import authenticate, login, logout
# from rest_framework import status

# from rest_framework import generics
# from django.contrib.auth.models import User
# from rest_framework.permissions import IsAuthenticated, IsAdminUser
# from rest_framework.decorators import api_view

# from .models import *
# from .serializer import *


# ## Login View 
# class LoginAPIView(APIView):

#     def post(self, request):
#         data = request.data
#         serializer = LoginSerializers(data=data)
#         if not serializer.is_valid():
#             return Response({
#                 "status": False,
#                 "data": serializer.data
#             })
#         username = serializer.data['username']
#         password = serializer.data['password']

#         user_obj = authenticate(username=username, password=password)
#         if user_obj is None:
#             return Response({"error": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)
        
#         if user_obj.is_active:
#             token, created = Token.objects.get_or_create(user=user_obj)
#             return Response({"token": token.key}, status=status.HTTP_200_OK)
#         else:
#             return Response({"error": "User is inactive"}, status=status.HTTP_400_BAD_REQUEST)

# class LogoutView(APIView):
#     def post(self, request):
#         if request.user.is_authenticated:
#             # Delete token if authenticated
#             request.user.auth_token.delete()
#             return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
#         else:
#             # Handle unauthenticated users
#             return Response({"detail": "User is not authenticated."}, status=status.HTTP_200_OK)

# class CreateUserView(generics.ListCreateAPIView):
#     model = get_user_model()
#     # authentication_classes = [SessionAuthentication]
#     # permission_classes = [IsAdminUser]
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
    
        
# ### FOR DELETE USERS
# class UserDeleteAPIView(APIView):
#     permission_classes = [IsAdminUser]  # Only admins can delete users

#     def delete(self, request, user_id):
#         try:
#             user = User.objects.get(id=user_id)
#             user.delete()
#             return Response({"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
#         except User.DoesNotExist:
#             return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    
# ### For Api Test 
# @api_view(["GET"])
# def FazalSons(request):
#     return Response("Backend in Working Fine")
    
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view
from .models import *
from .serializer import *


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
    
        
### FOR DELETE USERS
class UserDeleteAPIView(APIView):
    # permission_classes = [IsAdminUser]  # Only admins can delete users

    def delete(self, request, user_id):
         # Check if the user is trying to delete themselves
        if request.user.id == int(user_id):
            return Response("You cannot delete your own account.", status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(id=user_id)
            username = User.username
            username = User.username
            user.delete()
            return Response(f"User {username} deleted successfully.", status=status.HTTP_204_NO_CONTENT)
            return Response(f"User {username} deleted successfully.", status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response("User not found.", status=status.HTTP_404_NOT_FOUND)
        
# class AddSystemRoleView(generics.ListCreateAPIView):
#     # permission_classes = [IsAdminUser]
#     queryset = SystemRole.objects.all()
#     serializer_class = SystemRoleSerializer
#     pagination_class = None

    
@api_view(['GET'])
def GetPermissionsView(request):
        permission = CustomPermissions.objects.all()
        serializer = PermissionSerializer(permission, many=True)
        return Response(serializer.data)

    
@api_view(['GET', 'POST'])
def AddSystemRoleView(request):
   
    if request.method == 'GET':
        system_role = SystemRole.objects.all()
        serializer = SystemRoleSerializer(system_role, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PostSystemRoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

class ActionSystemRoleView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAdminUser]
    queryset = SystemRole.objects.all()
    serializer_class = PostSystemRoleSerializer
  
    
@api_view(["GET"])
def FetchSystemRoleView(request):
    if request.method == 'GET':
        system_role = SystemRole.objects.all()
        serializer = FetchSystemRoleSerializer(system_role, many=True)
        return Response(serializer.data)

    
    
### For Api Test 
@api_view(["GET"])
def FazalSons(request):
    return Response("Backend in Working Fine")
    