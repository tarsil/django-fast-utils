from datetime import datetime

from django.conf import settings
from django.http import HttpResponse
from django.middleware import csrf
from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import LoginSerializer


def get_tokens_for_user(user):
    """
    Gets the token for a given user using JWT
    """
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh)
    }


class LoginJWTApiView(APIView):
    """
    User login for JWT
    """
    serializer_class = LoginSerializer

    def get_timestamp(self, last_login):
        return datetime.timestamp(last_login)

    def set_cookie(self, response, key, value, max_age, expires, secure, httponly, samesite):
        now = datetime.utcnow()
        max_age = self.get_timestamp(now + max_age)
        expires = now + expires

        response.set_cookie(
            key=key, value=value, max_age=max_age, expires=expires, secure=secure, httponly=httponly,
            samesite=samesite
        )
        return response

    def process_access_token(self, response, data):
        """
        Processes a JWT access token
        """
        response = self.set_cookie(
            response,
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=data["access"],
            max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
        return response

    def process_refresh_token(self, response, data):
        """
        Processes a JWT refresh token
        """
        response = self.set_cookie(
            response,
            key=settings.SIMPLE_JWT['REFRESH_COOKIE'],
            value=data["refresh"],
            max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['REFRESH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['REFRESH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['REFRESH_COOKIE_SAMESITE']
        )
        return response

    def assert_values(self):
        """
        Checks if the values needed for the login are in the settings.
        """
        assert hasattr(settings, 'SIMPLE_JWT'), (
            'SIMPLE_JWT is not in the settings.'
        )

        values = [
            'AUTH_COOKIE',
            'ACCESS_TOKEN_LIFETIME',
            'AUTH_COOKIE_SECURE',
            'AUTH_COOKIE_HTTP_ONLY',
            'AUTH_COOKIE_SAMESITE',
            'REFRESH_COOKIE',
            'REFRESH_TOKEN_LIFETIME',
            'REFRESH_COOKIE_SECURE',
            'REFRESH_COOKIE_HTTP_ONLY',
            'REFRESH_COOKIE_SAMESITE'
        ]

        for value in values:
            assert value in settings.SIMPLE_JWT, (
                "The %s is not in SIMPLE_JWT settings." % value
            )


    def post(self, request, format=None):
        """
        Gets an email and a password, sanitizes and log a user.
        """
        self.assert_values()

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = Response()

        # GETS THE USER
        user = serializer.get_user()

        if user is None or not user:
            return Response({
                'detail': 'Invalid email or password.'
            }, status=status.HTTP_404_NOT_FOUND)

        # CHECK ACTIVE USER
        if not user.is_active:
            return Response({
                'detail': 'This account is not active.'
            }, status=status.HTTP_404_NOT_FOUND)

        data = get_tokens_for_user(user)
        response = self.process_access_token(response, data)
        response = self.process_refresh_token(response, data)

        # UPDATES CSRF
        csrf.get_token(request)
        response.data = data
        return response


class LogoutJWTApiView(APIView):

    def post(self, request):
        """
        Logs out of the system and removes the cookie.
        """
        response = Response()
        response.delete_cookie(key="csrftoken")
        response.delete_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE']
        )
        response.delete_cookie(
            key=settings.SIMPLE_JWT['REFRESH_COOKIE']
        )
        return response
