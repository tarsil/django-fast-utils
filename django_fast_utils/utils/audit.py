"""
For auditing models.
"""

from django.conf import settings
from django.db import models

exclude = ["created_at", "created_by", "updated_at", "updated_by"]

CREATED_AT = "created_%(class)s_set"
MODIFIED_AT = "modified_%(class)s_set"


class GeneralDateTimeModel(models.Model):
    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    updated_at = models.DateTimeField(null=False, blank=False, auto_now=True)

    class Meta:
        abstract = True


class IndexGeneralDateTimeModel(models.Model):
    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(null=False, blank=False, auto_now=True, db_index=True)

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name=CREATED_AT,
        null=False,
        blank=True,
        on_delete=models.DO_NOTHING,
    )
    updated_at = models.DateTimeField(null=False, blank=False, auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name=MODIFIED_AT,
        null=False,
        blank=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        abstract = True


class GeneralTimeStampedModel(models.Model):
    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name=CREATED_AT,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
    )
    updated_at = models.DateTimeField(null=False, blank=False, auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name=MODIFIED_AT,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        abstract = True


class IndexedGeneralTimeStampedModel(models.Model):
    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True, db_index=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name=CREATED_AT,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
    )
    updated_at = models.DateTimeField(null=False, blank=False, auto_now=True, db_index=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name=MODIFIED_AT,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        abstract = True