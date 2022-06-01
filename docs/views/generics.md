# Generics

Mixins that can be used to optimise some of the querysets.

## SelectRelatedMixin

Optimises the queryset on a SQL level. [More information](https://docs.djangoproject.com/en/4.0/ref/models/querysets/#select-related).

### How to use

```python
from django.db import models
from django_fast_utils.views.generics import SelectRelatedMixin
from rest_framework.generics import ListAPIView


class MyView(SelectRelatedMixin, ListAPIView):
    select_related = ['company', 'company__user']

```

## PrefetchRelatedMixin

Optimises the queryset on a Pythonic level. [More information](https://docs.djangoproject.com/en/4.0/ref/models/querysets/#prefetch-related).

### How to use

```python
from django.db import models
from django_fast_utils.views.generics import PrefetchRelatedMixin
from rest_framework.generics import ListAPIView


class MyView(PrefetchRelatedMixin, ListAPIView):
    prefetch_related = ['company', 'company__user']

```
