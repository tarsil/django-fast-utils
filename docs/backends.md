# Backends

## Email Backend

Authentication backend that uses the `email` instead of the `username` for the logins.

### How to use

In your `settings.py` file, add the following.

```python

AUTHENTICATION_BACKENDS = (
    ...
    "django_fast_utils.backends.EmailBackend",
)
```

You can now use the email to login into your application using the `authenticate` django
standard.

## Example

Using [Django Rest framework](https://www.django-rest-framework.org/).

- `views.py`

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer


class LoginApiView(APIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_user()
        login(request, user)

        return Response(status=status.HTTP_200_OK)

```

- `serializers.py`

```python
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(allow_blank=False, required=True)
    password = serializers.CharField(allow_blank=False, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auth_user = None

    def get_user(self):
        return self.auth_user

    def validate(self, attrs):
        try:
            email = attrs["email"].strip()
            password = attrs["password"]
            try:
                self.auth_user = authenticate(email=email, password=password)
            except ValueError:
                self.auth_user = None

            if self.auth_user:
                return attrs

        except (accounts.models.HubUser.DoesNotExist, KeyError):
            raise serializers.ValidationError(_("Your login details were incorrect. Please try again."))
```
