from rest_framework.permissions import BasePermission




class IsAdmin(BasePermission):
    """
    Allows access only to users with the 'Admin' role.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False
        # Check if the user has the 'Admin' role
        if hasattr(request.user, 'userprofile') and request.user.userprofile.system_roles.filter(
            permissions__permission_name='Admin'
        ).exists():
            return True
        return False