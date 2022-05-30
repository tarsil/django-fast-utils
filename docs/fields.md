# Fields

Custom fields to be used within `models` or `serializers` of any django application using
[Django Rest framework](https://www.django-rest-framework.org/).

## ChoicesField

Django provides a choices inside the CharField with the attribute `choices`. This field allows direct
declaration in the models.

### How to use

```python
from django_fast_utils.fields import ChoicesField
from django.db import models


class MyModel(models.Model):
    custom_choices = ChoiceField(choices=MY_CHOICES)
    ...
```

## WritableSerializerMethodField

Custom version of `SerializerMethodField` from [Django Rest framework](https://www.django-rest-framework.org/)
that allows read/write.

### How to use

```python
from django_fast_utils.fields import WritableSerializerMethodField
from rest_framwork import serializers


class MySerializer(serializers.Serializer):
    name = WritableSerializerMethodField()

    def get_name(self, instance):
        ...
        ...
```

## AbsoluteImageField

When serializing an ImageField url usually implies some extra code to show the full path url
and expose the full url into APIs.

### How to use

```python
from django_fast_utils.fields import AbsoluteImageField
from rest_framwork import serializers


class MySerializer(serializers.Serializer):
    photo = AbsoluteImageField()

```
