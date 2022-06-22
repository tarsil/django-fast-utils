"""
All things middleware
"""
from datetime import datetime

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from rest_framework import HTTP_HEADER_ENCODING
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken

from .. import settings as api_settings

AUTH_HEADER_TYPES = settings.SIMPLE_JWT['AUTH_HEADER_TYPES']

AUTH_HEADER_TYPE_BYTES = set(
    h.encode(HTTP_HEADER_ENCODING)
    for h in AUTH_HEADER_TYPES
)

if settings.SIMPLE_JWT['BLACKLIST_AFTER_ROTATION']:
    from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken


def validate_and_refresh(refresh_token):
    """
    Validates the refresh token and sets the new token.
    """
    refresh = RefreshToken(refresh_token)
    data = {"access": str(refresh.access_token)}

    if settings.SIMPLE_JWT['ROTATE_REFRESH_TOKENS']:
        if settings.SIMPLE_JWT['BLACKLIST_AFTER_ROTATION']:
            try:
                refresh.blacklist()
            except AttributeError:
                pass

        refresh.set_jti()
        refresh.set_exp()
        refresh.set_iat()

        data['refresh'] = str(refresh)

    return data


def validate_token(token):
    """
    Verifies if a token sent is valid.
    """
    try:
        token = UntypedToken(token)
    except TokenError as e:
        return InvalidToken(e.args[0])

    if (
        settings.SIMPLE_JWT['BLACKLIST_AFTER_ROTATION']
        and "rest_framework_simplejwt.token_blacklist" in settings.INSTALLED_APPS
    ):
        jti = token.get(settings.SIMPLE_JWT['JTI_CLAIM'])
        if BlacklistedToken.objects.filter(token__jti=jti).exists():
            raise ValidationError("Token is blacklisted")

    return {}


class JWTRefreshRequestCookies(MiddlewareMixin):
    """
    Refreshes the cookie if exists in the request and
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app_settings = settings if hasattr(settings, 'DJANGO_FAST_UTILS') else api_settings

    def get_timestamp(self, date_to_parse):
        """
        Converts a date into timestamp.
        """
        return datetime.timestamp(date_to_parse)

    def get_header(self, request):
        """
        Extracts the header containing the JSON web token from the given
        request.
        """
        header = request.META.get(settings.SIMPLE_JWT['AUTH_HEADER_NAME'])

        if isinstance(header, str):
            # Work around django test client oddness
            header = header.encode(HTTP_HEADER_ENCODING)

        return header

    def set_cookie(self, response, key, value, max_age, expires, secure, httponly, samesite):
        """
        Adds the cookie to the client
        """
        now = datetime.utcnow()
        max_age = self.get_timestamp(now + max_age)
        expires = now + expires

        response.set_cookie(
            key=key, value=value, max_age=max_age, expires=expires, secure=secure, httponly=httponly,
            samesite=samesite
        )
        return response

    def refresh(self, refresh_token):
        """
        Validates and refreshes the access token
        """
        try:
            data = validate_and_refresh(refresh_token)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return data

    def exclude_from_request(self, request):
        """
        Extracts the full path information.
        """
        return request.get_full_path_info()

    def handle_request(self, request):
        """
        Handles the request for the acess an and refresh token.
        """
        access_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE']) or None
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['REFRESH_COOKIE']) or None
        data = {}

        if access_token:
            is_valid = validate_token(access_token)

            if hasattr(is_valid, 'default_code'):
                if is_valid.default_code == 'token_not_valid':
                    if refresh_token:
                        data = self.refresh(refresh_token)
                        request.COOKIES[settings.SIMPLE_JWT['AUTH_COOKIE']] = data[settings.SIMPLE_JWT['AUTH_COOKIE']]
        else:
            if refresh_token:
                data = self.refresh(refresh_token)
                request.COOKIES[settings.SIMPLE_JWT['AUTH_COOKIE']] = data[settings.SIMPLE_JWT['AUTH_COOKIE']]

    def handle_response(self, request, response):
        """
        Handles the response for the cookie.
        """
        access_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE']) or None

        if not access_token:
            return response

        self.set_cookie(
            response,
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=access_token,
            max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
        return response

    def process_request(self, request):
        """
        Processes the request by checking the headers of the request and if the tokens
        are present in the cookies.

        1. Checks for the access token
        2. Validates the token
        3. Refreshes the token
        4. Adds it back to the headers
        """
        assert 'LOGOUT_URL' in self.app_settings.DJANGO_FAST_UTILS, (
            "'LOGOUT_URL' key is missing from the settings."
        )
        assert isinstance(self.app_settings.DJANGO_FAST_UTILS['LOGOUT_URL'], list), (
            f"'LOGOUT_URL' should be a list and not {type(self.app_settings.DJANGO_FAST_UTILS['LOGOUT_URL'])}."
        )

        url = self.exclude_from_request(request)
        if url not in self.app_settings.DJANGO_FAST_UTILS['LOGOUT_URL']:
            return self.handle_request(request)

    def process_response(self, request, response):
        """
        Sends the new access token to the client.
        """
        url = self.exclude_from_request(request)
        if url not in self.app_settings.DJANGO_FAST_UTILS['LOGOUT_URL']:
            return self.handle_response(request, response)
        return self.get_response(request)
