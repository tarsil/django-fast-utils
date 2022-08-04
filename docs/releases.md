# Releases

## 2.0.4

- Fixed code smell in `get_prep_value` from `ListField`.

## 2.0.3

- Fixed middleware validation and verification.
- Added `DJANGO_FAST_UTILS` settings.
- Added `LogoutJWTApiView`.

## 2.0.2

- Changed imports.

## 2.0.1

- Added missing requirement.

## 2.0.0

- Added `LoginJWTApiView` allowing the JWT Token being protected via `httpOnly=true` cookie
  and refreshing the token via `middleware`. [Docs here](./views/auth.md).

## 1.0.3

- Fixed typo in `PrefetchRelatedMixin`.

## 1.0.2

- Add `SelectRelatedMixin` and `PrefetchRelatedMixin` for generic views.

## 1.0.1

- Fix `django-guardian` dependency.

## 1.0.0

- Initial release of `django-fast-utils`.
