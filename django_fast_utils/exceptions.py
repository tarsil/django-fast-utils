from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.exceptions import _get_error_details


class ValidationException(APIException):
    """
    Wrapper over APIException being more flexible with the core
    """
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _('Invalid input.')
    default_code = 'invalid'

    def __init__(self, detail=None, code=None, status_code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code
        self.status_code = status_code or self.status_code

        # For validation failures, we may collect many errors together,
        # so the details should always be coerced to a list if not already.
        if not isinstance(detail, dict) and not isinstance(detail, list):
            detail = {"detail": detail}

        self.detail = _get_error_details(detail, code)


class ValidationError(ValidationException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Invalid input.')
    default_code = 'invalid'


class NotAuthorized(ValidationException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('You do not have permission to perform this action.')
    default_code = 'not_authorized'


class PermissionDenied(ValidationException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _('You do not have permission to perform this action.')
    default_code = 'not_allowed'
