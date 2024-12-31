
from rest_framework.permissions import BasePermission

class IsProduct(BasePermission):
    def has_permission(self, request, view):
         ## Check if the user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False
           
        ## Check if the user has the 'Customer' role
        if hasattr(request.user, 'userprofile') and request.user.userprofile.system_roles.filter(
            permissions__permission_name='Admin'
        ).exists():
            return True
        
        
           # Check if the user has the required 'CustomerAdmin' permission via their role
        if hasattr(request.user, 'userprofile'):
            has_customer_permission = request.user.userprofile.system_roles.filter(
                permissions__permission_name='Product'
            ).exists()
            if not has_customer_permission:
                return False
        else:
            # Deny access if userprofile is missing
            return False

        # Allow only specific methods: POST (add), PUT/PATCH (edit), and safe methods (e.g., GET)
        if request.method in ['POST', 'PUT', 'PATCH', 'GET', 'HEAD', 'OPTIONS']:
            return True

        # Explicitly deny DELETE requests
        if request.method == 'DELETE':
            return False
        return False