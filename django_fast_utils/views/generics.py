"""
Useful addons to be used in the
"""
from django.db.models.query import QuerySet
from rest_framework.generics import GenericAPIView, ListAPIView


class SelectRelatedMixin(GenericAPIView):
    select_related = None

    def get_queryset(self):
        assert self.model is not None, (
            "'%s' should include a `model` attribute, "
            "or override the `get_model()` method."
            % self.__class__.__name__
        )

        assert self.select_related is None or (
            isinstance(self.select_related, list) or isinstance(self.select_related, tuple)
            ), (
            "'select_related' must be a list and not %s." % type(self.select_related)
        )

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            queryset = queryset.select_related(*self.select_related).all()
        return queryset


class PrefetchRelatedMixin(GenericAPIView):
    prefetch_related = None

    def get_queryset(self):
        assert self.model is not None, (
            "'%s' should include a `model` attribute, "
            "or override the `get_model()` method."
            % self.__class__.__name__
        )

        assert self.prefetch_related is None or (
            isinstance(self.prefetch_related, list) or isinstance(self.prefetch_related, tuple)
            ), (
            "'prefetch_related' must be a list and not %s." % type(self.prefetch_related)
        )

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            queryset = queryset.all()
            queryset = queryset.prefetch_related(*self.prefetch_related)
        return queryset
