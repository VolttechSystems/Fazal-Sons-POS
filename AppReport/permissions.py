from rest_framework.permissions import BasePermission

class IsReportUser(BasePermission):
    """
    Allows access only to users with the 'Cashier' role.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False
        # # Check if the user has the 'TransactionAdmin' role
        if hasattr(request.user, 'userprofile') and request.user.userprofile.system_roles.filter(
            permissions__permission_name='Reports'
        ).exists():
            # TransactionAdmin have full access, including DELETE
            return True
        # Deny access for any other methods not explicitly allowed
        return False
    