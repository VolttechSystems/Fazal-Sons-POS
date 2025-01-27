from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import api_view
from .models import *
from .serializer import *
from AppProduct.views import MyLimitOffsetPagination
from django.http import JsonResponse
import random
import string
from django.contrib.auth.models import User

## Login View
class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        print(data)
        serializer = LoginSerializers(data=data)

        if not serializer.is_valid():
            return Response({
                "status": False,
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.data['username']
        password = serializer.data['password']

        user_obj = authenticate(username=username, password=password)
        if user_obj is None:
            return Response({"error": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)

        if not user_obj.is_active:
            return Response({"error": "User is inactive"}, status=status.HTTP_400_BAD_REQUEST)

        # Generate token
        token, created = Token.objects.get_or_create(user=user_obj)

        # Check if the user is a superuser
        if user_obj.is_superuser:
            # Ensure Super_Super_Admin role exists
            admin_role, created = SystemRole.objects.get_or_create(
                sys_role_name='Super_Super_Admin',
                defaults={
                    'status': 'Active',
                    'created_by': 'System',  # Default creator
                }
            )

            # Assign all permissions to the Admin role if it was just created
            if created:
                all_permissions = CustomPermissions.objects.filter(permission_name='SuperAdmin')
                admin_role.permissions.set(all_permissions)

            # Ensure the role is active
            if admin_role.status != 'Active':
                admin_role.status = 'Active'
                admin_role.save()

            # Assign Admin role to the superuser
            user_profile, _ = UserProfile.objects.get_or_create(user=user_obj)
            user_profile.system_roles.add(admin_role)

            # Superuser gets all outlets
            all_outlets = Outlet.objects.values('id', 'outlet_name')
            user_outlets = [{'id': outlet['id'], 'outlet_name': outlet['outlet_name']} for outlet in all_outlets]

            # Include Admin role with all permissions
            system_role = [{
                'id': admin_role.id,
                'sys_role_name': admin_role.sys_role_name,
                'permissions': admin_role.permissions.values('id', 'permission_name')
            }]
            return Response({
            "shop": "Volttech",
            "username": user_obj.username,
            "token": token.key,
            "outlet": user_outlets,
            "System_role": system_role}, status=status.HTTP_200_OK)
        if not user_obj.is_superuser and user_obj.is_staff:
            # Ensure Super_Super_Admin role exists
            admin_role, created = SystemRole.objects.get_or_create(
                sys_role_name='Admin',
                # shop_id=
                defaults={
                    'status': 'Active',
                    'created_by': 'System',  # Default creator
                }
            )

            # Assign all permissions to the Admin role if it was just created
            if created:
                all_permissions = CustomPermissions.objects.exclude(permission_name='SuperAdmin')
                admin_role.permissions.set(all_permissions)

            # Ensure the role is active
            if admin_role.status != 'Active':
                admin_role.status = 'Active'
                admin_role.save()

            # Assign Admin role to the superuser
            user_profile, _ = UserProfile.objects.get_or_create(user=user_obj)
            user_profile.system_roles.add(admin_role)

            # Superuser gets all outlets
            all_outlets = Outlet.objects.filter(shop_id=user_profile.shop.id).values('id', 'outlet_name')
            user_outlets = [{'id': outlet['id'], 'outlet_name': outlet['outlet_name']} for outlet in all_outlets]

            # Include Admin role with all permissions
            system_role = [{
                'id': admin_role.id,
                'sys_role_name': admin_role.sys_role_name,
                'permissions': admin_role.permissions.values('id', 'permission_name')
            }]
            return Response({
            "shop": user_profile.shop.name,
            "shop_id": user_profile.shop.id,
            "username": user_obj.username,
            "token": token.key,
            "outlet": user_outlets,
            "System_role": system_role}, status=status.HTTP_200_OK)
 
        else:
            # Non-superusers and Non-staff get their specific outlets and roles
            user_profile = UserProfile.objects.get(user_id=user_obj.id)
            outlets = user_profile.outlet.values('id', 'outlet_name')
            user_outlets = [{'id': outlet['id'], 'outlet_name': outlet['outlet_name']} for outlet in outlets]

            # Fetch active system roles and permissions
            system_role_names = user_profile.system_roles.all().values('id', 'sys_role_name')
            system_role = [
                {
                    'id': role['id'],
                    'sys_role_name': role['sys_role_name'],
                    'permissions': user_profile.system_roles.get(id=role['id']).permissions.values('id', 'permission_name')
                }
                for role in system_role_names
            ]

        return Response({
            "shop": user_profile.shop.name,
            "shop_id": user_profile.shop.id,
            "username": user_obj.username,
            "token": token.key,
            "outlet": user_outlets,
            "System_role": system_role
        }, status=status.HTTP_200_OK)

        

class LogoutView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            # Delete token if authenticated
            request.user.auth_token.delete()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        else:
            # Handle unauthenticated users
            return Response({"detail": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'POST'])
def CreateUserView(request, shop):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        users = UserProfile.objects.filter(user__is_superuser=False, user__is_staff=False, shop_id=shop).select_related('user').prefetch_related('system_roles', 'outlet')
        serializer = UserProfileSerializer(users, many=True)
        paginator = MyLimitOffsetPagination()
        paginated_query = paginator.paginate_queryset(serializer.data, request)
        return paginator.get_paginated_response(paginated_query)
    
@api_view(['GET','PATCH'])
def UpdateUserView(request, shop, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
         return Response("User Not Found", status=status.HTTP_400_BAD_REQUEST)
        
    user_profile = user.userprofile
    if not user_profile.shop_id == int(shop):
        return Response('No User Found in Shop')
    if request.method == 'PATCH':
        serializer = UserSerializer(user, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        try:
            users = UserProfile.objects.get(user__id=user_id, user__is_superuser=False, user__is_staff=False, shop_id=shop)
        except UserProfile.DoesNotExist:
            return Response("User Profile Not Found",  status=status.HTTP_400_BAD_REQUEST)
        serializer = UserProfileSerializer(users)
        return Response(serializer.data)
        
### FOR DELETE USERS
class UserDeleteAPIView(APIView):
    # permission_classes = [IsAdminUser]  # Only admins can delete users

    def delete(self, request, user_id):
         # Check if the user is trying to delete themselves
        if request.user.id == int(user_id):
            return Response("You cannot delete your own account.", status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return Response("User deleted successfully.", status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response("User not found.", status=status.HTTP_404_NOT_FOUND)
            
@api_view(['GET'])
def GetPermissionsView(request):
        permission = CustomPermissions.objects.exclude(permission_name='SuperAdmin')
        serializer = PermissionSerializer(permission, many=True)
        return Response(serializer.data)

class AdminChangePasswordView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Ensure the requesting user is an admin
        # if not request.user.is_staff:
        #     return Response(
        #         {"error": "You do not have permission to perform this action."},
        #         status=status.HTTP_403_FORBIDDEN,
        #     )

        serializer = AdminChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            # Fetch the user
            user_id = serializer.validated_data['user_id']
            new_password = serializer.validated_data['new_password']
            user = User.objects.get(id=user_id)

            user.set_password(new_password)
            user.save()

            return Response({"message": f"Password for user {user} has been changed successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def check_username(request):
    username = request.query_params.get('username', '')
    if not username:
        return Response({"error": "Username is required"}, status=400)
    is_taken = User.objects.filter(username=username).exists()
    # Generate suggestions if taken
    suggestions = []
    if is_taken:
        for _ in range(3):  # Generate 5 suggestions
            random_suffix = ''.join(random.choices(string.digits, k=3))
            suggestions.append(f"{username}{random_suffix}")

    return Response({"is_taken": is_taken, "suggestions": suggestions})

    
@api_view(['GET', 'POST'])
def AddSystemRoleView(request, shop):
    try:
        check_shop = Shop.objects.get(id=shop)
    except Shop.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
   
    if request.method == 'GET':
        system_role = SystemRole.objects.filter(shop_id=shop)
        serializer = SystemRoleSerializer(system_role, many=True)
        # return Response(serializer.data)
        paginator = MyLimitOffsetPagination()
        paginated_system_roles = paginator.paginate_queryset(serializer.data, request)
        return paginator.get_paginated_response(paginated_system_roles)

    elif request.method == 'POST':
        serializer = PostSystemRoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

class ActionSystemRoleView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSystemRoleSerializer
    def get_queryset(self):
        get_shop = self.kwargs.get('shop')
        system_role = SystemRole.objects.filter(shop_id=get_shop).prefetch_related('permissions')
        return system_role
  
    
@api_view(["GET"])
def FetchSystemRoleView(request, shop):
    try:
        check_shop = Shop.objects.get(id=shop)
    except Shop.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
   
    if request.method == 'GET':
        system_role = SystemRole.objects.filter(shop_id=shop)
        serializer = FetchSystemRoleSerializer(system_role, many=True)
        return Response(serializer.data)

    
    
### For Api Test 
@api_view(["GET"])
def FazalSons(request):
    return Response("Backend in Working Fine")
    