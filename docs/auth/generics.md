# Auth

[Django Rest framework](https://www.django-rest-framework.org/) provides a set of abstractions
on the top of django.

This package provides an abstraction on the top of Django Rest framework.

## AnonymousAuthentication

Mixin for anonymous users.

## How to use

```python
from django_fast_utils.auth.generics import AnonymousAuthentication
from rest_framework.views import APIView


class MyView(AnonymousAuthentication, APIView):
    pass

```

## AuthMixin

Django rest framework doesn't append permission_classes on inherited models which can bring issues when
it comes to call an API programmatically, this way we create a metaclass that will read from a property custom
from our subclasses and will append to the default `permission_classes`.

## How to use

```python
from django_fast_utils.auth.generics import AuthMixin
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser


class MyView(AuthMixin, APIView):
    permissions = [IsAdminUser]


MyView.permissions # Returns IsAuthenticated (default from AuthMixin) and IsAdminUser

```

Django Fast Utils allows to extend the `permissions` on every inherited view without overriding anything.

## NoPermissionsMixin

No permissions applied to the views. Only used when no permissions (auth) is not needed for
specific cases.

## RequiredUserContextView

Used to inject the `request.user` into serializers when needed.

### How to use

```python
from django_fast_utils.auth.generics import RequiredUserContextView


class MyView(RequiredUserContextView, ListAPIView):
    ...


class MySecondView(RequiredUserContextView, APIView):

    def post(self, request, *args, **kwargs):
        serializer = MySerializer(data=request.data, context=self.get_serializer_context())

```
