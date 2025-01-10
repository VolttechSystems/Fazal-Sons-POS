from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CustomTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        auth = request.headers.get('Authorization', '')

        if auth.lower() == 'token null':  # Treat 'null' as no token
            return None  # Skip authentication, proceed as unauthenticated

        return super().authenticate(request)
