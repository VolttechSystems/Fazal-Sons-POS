from rest_framework.permissions import BasePermission

class IsCashier(BasePermission):
    """
    Allows access only to users with the 'Cashier' role.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False

        # Check if the user has a UserProfile and the 'Cashier' role
        if hasattr(request.user, 'userprofile'):
            return request.user.userprofile.system_roles.filter(sys_role_name='Cashier').exists()

        return False
