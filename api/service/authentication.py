from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.utils import timezone


class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise AuthenticationFailed('User inactive or deleted')

        # This is required for the time comparison
        token_age = (timezone.now() - token.created).seconds
        if token_age > settings.TOKEN_EXPIRE_TIME:
            token.delete()
            raise AuthenticationFailed('Token has expired')

        return token.user, token
