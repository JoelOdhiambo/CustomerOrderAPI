import requests
from jose import jwt
from jose.exceptions import JWTError
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

class Auth0JSONWebTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization', None)

        if not auth_header:
            return None

        parts = auth_header.split()

        if parts[0].lower() != 'bearer':
            raise AuthenticationFailed('Authorization header must start with Bearer')
        elif len(parts) == 1:
            raise AuthenticationFailed('Token not found')
        elif len(parts) > 2:
            raise AuthenticationFailed('Authorization header must be Bearer token')

        token = parts[1]
        try:
            jwks_url = f'https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json'
            jwks = requests.get(jwks_url).json()
            unverified_header = jwt.get_unverified_headers(token)
            rsa_key = {}
            for key in jwks['keys']:
                if key['kid'] == unverified_header['kid']:
                    rsa_key = {
                        'kty': key['kty'],
                        'kid': key['kid'],
                        'use': key['use'],
                        'n': key['n'],
                        'e': key['e']
                    }
            if rsa_key:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=['RS256'],
                    audience=settings.AUTH0_AUDIENCE,
                    issuer=f'https://{settings.AUTH0_DOMAIN}/'
                )
                return (payload, token)
        except JWTError:
            raise AuthenticationFailed('Token is invalid')

        return None
