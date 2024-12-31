from rest_framework.permissions import BasePermission

class IsTransaction(BasePermission):
    """
    Allows access only to users with the 'Cashier' role.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False
        # # Check if the user has the 'TransactionAdmin' role
        if hasattr(request.user, 'userprofile') and request.user.userprofile.system_roles.filter(
            permissions__permission_name='Admin'
        ).exists():
            # TransactionAdmin have full access, including DELETE
            return True

        # Check if the user has the required 'Transaction' permission via their role
        if hasattr(request.user, 'userprofile'):
            has_transaction_permission = request.user.userprofile.system_roles.filter(
                permissions__permission_name='Transaction'
            ).exists()
            if not has_transaction_permission:
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

        # Deny access for any other methods not explicitly allowed
        return False
    