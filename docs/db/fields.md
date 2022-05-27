# Database

Custom fields to be used within the models.

## ListField

Save lists in python format directly.

### How to use

```python
from django.db import models
from django_fast_utils.db.fields import ListField


class MyModel(models.Model):
    my_list = ListField()
    ...
```
