# Audit

Mixins that injects fields into django models allowing the audit trailing.

## GeneralDateTimeModel

Adds only `created_at` and `updated_at`

### How to use

```python
from django.db import models
from django_fast_utils.utils.audit import GeneralDateTimeModel


class MyModel(GeneralDateTimeModel):
    ...

```

## IndexGeneralDateTimeModel

Adds only `created_at` as index and `updated_at` as index.

### How to use

```python
from django.db import models
from django_fast_utils.utils.audit import IndexGeneralDateTimeModel


class MyModel(IndexGeneralDateTimeModel):
    ...

```

## TimeStampedModel

Adds `created_at`, `updated_at`, `created_by` and `updated_by` to the model and `created_by` and `updated_by`
**are mandatory**.

`created_by` and `updated_by` are FK to the `settings.AUTH_USER_MODEL`.

### How to use

```python
from django.db import models
from django_fast_utils.utils.audit import TimeStampedModel


class MyModel(TimeStampedModel):
    ...

```

## GeneralTimeStampedModel

Adds `created_at`, `updated_at`, `created_by` and `updated_by` to the model and `created_by` and `updated_by`
are **not mandatory**.

`created_by` and `updated_by` are FK to the `settings.AUTH_USER_MODEL`.

### How to use

```python
from django.db import models
from django_fast_utils.utils.audit import GeneralTimeStampedModel


class MyModel(GeneralTimeStampedModel):
    ...

```

## IndexedGeneralTimeStampedModel

Adds `created_at`, `updated_at`, `created_by` and `updated_by` to the model and `created_by` and `updated_by`
are **not mandatory**.

`created_by` and `updated_by` are FK to the `settings.AUTH_USER_MODEL`.

### How to use

```python
from django.db import models
from django_fast_utils.utils.audit import IndexedGeneralTimeStampedModel


class MyModel(IndexedGeneralTimeStampedModel):
    ...

```
