# Permissions

Django Fast Utils uses [Django Guardian](https://django-guardian.readthedocs.io/en/stable/)
to manipulate the permissions of objects.

## How to use

- Add `django-guardian` to your project `settings.py`.

```python

INSTALLED_APPS = (
    # ...
    'guardian'
)

AUTHENTICATION_BACKENDS = (
    ...
    'guardian.backends.ObjectPermissionBackend',
    ...
)

```

- Use in your code.

```python
from django_fast_utils.permissions import assign_user_perm


assign_user_perm('is_super_user', user, cars) # (Default value = False)
user.has_perm('is_super_user', user) # True

```

Django guardian by default creates an anonymous user and that can be disabled in the
`settings.py`.

```python

ANONYMOUS_USER_NAME = None

```
