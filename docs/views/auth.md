# Authentication with JWT

JWT (JSON Web Token) is widely used for authentication but with that also brings certain
level of concerns such as where to store the access and refresh tokens.

There are multiple ways:

1. Local Storage - Prompt for XSS attacks.
2. Session Storage - Deplects the UX of a user as it needs to login on each tab session.
3. Cookie - Limited but with specific options and safer using `httpOnly = True`.

Django Fast Utils covers the Cookies.

## Cookie httpOnly

When a cookie is set to httpOnly true, JavaScript cannot read and/or access those values
making the refresh and access tokens safer in the browser and reducing the attacks.

## Installation

Django Fast Utils uses [Django Rest Framework SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html)

### Settings

1. Add `rest_framework_simplejwt` and `rest_framework_simple_jwt.token_blacklist` to your `settings.py`

```python

INSTALLED_APPS = [
    ...
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    ...
]

```

2. Add the `django_fast_utils.auth.middleware.JWTRefreshRequestCookies' to `MIDDLEWARE`.

```python

MIDDLEWARE = [
    ...
    'django_fast_utils.auth.middleware.JWTRefreshRequestCookies',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    ...
]

```

3. Update your `REST_FRAMEWORK` settings.

```python
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_AUTHENTICATION_CLASSES": (
        ...
        ...
        'django_fast_utils.auth.backends.JWTCustomAuthentication',
    ),
}
```

4. Update the `SIMPLE_JWT` to have `django_fast_utils` settings for the authentication.

```python

SIMPLE_JWT = {
    ...
    # JWT FOR HTTP ONLY COOKIE SETTINGS
    'AUTH_COOKIE': 'access',  # Cookie name. Enables cookies if value is set.
    'AUTH_COOKIE_DOMAIN': None,     # A string like "example.com", or None for standard domain cookie.
    'AUTH_COOKIE_SECURE': True,    # Whether the auth cookies should be secure (https:// only).
    'AUTH_COOKIE_HTTP_ONLY' : True, # Http only cookie flag. It's not fetch by JS.
    'AUTH_COOKIE_PATH': '/',        # The path of the auth cookie.
    'AUTH_COOKIE_SAMESITE': 'Lax',  # Whether to set the flag restricting cookie leaks on cross-site requests. This can be 'Lax', 'Strict', or None to disable the flag.

    'REFRESH_COOKIE': 'refresh',  # Cookie name. Enables cookies if value is set.
    'REFRESH_COOKIE_DOMAIN': None,     # A string like "example.com", or None for standard domain cookie.
    'REFRESH_COOKIE_SECURE': True,    # Whether the auth cookies should be secure (https:// only).
    'REFRESH_COOKIE_HTTP_ONLY' : True, # Http only cookie flag.It's not fetch by JS.
    'REFRESH_COOKIE_PATH': '/',        # The path of the auth cookie.
    'REFRESH_COOKIE_SAMESITE': 'Lax',  # Flag restricting cookie leaks on cross-site requests. This can be 'Lax', 'Strict', or None to disable the flag.
}

```

5. Add the `LoginJWTApiView` and `LogoutJWTApiView` to your urls.

In your settings.py add `DJANGO_FAST_UTILS` setting:

```python
DJANGO_FAST_UTILS = {
    'LOGOUT_URL': ['/logout']
}
```

The `LOGOUT_URL` is expecting as list of possible `logout` urls used by the application.
This will ensure the middleware doesn't execute logic for specific views such as `refresh` of
tokens.

**Default**: `['/logout']`

```python
from django.urls import path
from django_fast_utils.views.auth.views import LoginJWTApiView, LogoutJWTApiView

urlpatterns = [
    ...
    path('login', LoginJWTApiView.as_view(), name='login'),
    path('logout', LoginJWTApiView.as_view(), name='logout')
    ...
]
```

**That's it!**. You can now login into your application using `email` and `password` and you
can see in your browser that the cookies are now set as httpOnly true.

## Refresh

Djago Fast Utils middleware handles with the automatic `refresh` of the token based on the
settings you added on the default `SIMPLE_JWT` settings.

```python

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=200),
    ...
}

```
