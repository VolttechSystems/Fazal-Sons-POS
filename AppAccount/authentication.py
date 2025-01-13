from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

# class CustomTokenAuthentication(TokenAuthentication):
#     def authenticate(self, request):
#         auth = request.headers.get('Authorization', '')

#         if auth.lower() == 'token null':  # Treat 'null' as no token
#             return None  # Skip authentication, proceed as unauthenticated

#         return super().authenticate(request)

class CustomTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        auth = request.headers.get('Authorization', '')

        # Ignore if the token is 'null'
        if auth.lower() == 'token null':
            return None  

        try:
            return super().authenticate(request)
        except AuthenticationFailed:
            # Ignore invalid tokens and proceed as unauthenticated
            return None
