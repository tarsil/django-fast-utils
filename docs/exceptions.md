# Exceptions

[Django Rest framework](https://www.django-rest-framework.org/) brings all the package
when it comes to validations but sometimes there is a need to have something more unique
and granular.

## ValidationException

The application on any level (view, model, serializer) can raise an exception similar to APIException
but with the possibility of providing different `status_code` and message details.

### How to use

```python
...
from django_fast_utils.exceptions import ValidationException

class MyView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(pk=1)
        except User.DoesNotExist:
            raise ValidationException(
                "User does not exist.",
                status_code=200
            )
```

## ValidationError

Same as as ValidationException with the default to `HTTP_400_BAD_REQUEST`.

## NotAuthorized

Same as as ValidationException with the default to `HTTP_401_UNAUTHORIZED`.

## PermissionDenied

Same as as ValidationException with the default to `HTTP_403_FORBIDDEN`.
