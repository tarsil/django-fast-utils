# Paginator

## NumberDetailPagination

[Django Rest framework](https://www.django-rest-framework.org/) provides standard paginator
classes but sometimes more details are needed to sent in the payload.

### Payload definition

```python
links': {
    'next': next page url,
    'previous': previous page url
    },
    'count': number of records fetched,
    'total_pages': total number of pages,
    'next': bool has next page,
    'previous': bool has previous page,
    'results': result set
})
```

### How to use

- View level:

```python
from django_fast_utils.paginator import NumberDetailPagination
...

class MyView(ListAPIView):
    pagination_class = NumberDetailPagination
    ...
```

- Making it global and default for all views with pagination:

```python
REST_FRAMEWORK = {
    ...
    "DEFAULT_PAGINATION_CLASS": "django_fast_utils.paginator.NumberDetailPagination"
    ...
}
```
