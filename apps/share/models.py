from core.models import BaseModel
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now
from django_extensions.db.fields import RandomCharField


class Guest(BaseModel):
    created_by = models.ForeignKey(
        verbose_name='생성자',
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name='guests',
    )
    code = RandomCharField(
        verbose_name='코드',
        length=12,
        unique=True,
    )
    access_scope = models.CharField(
        verbose_name='접근 범위',
        max_length=255,
    )
    expired_at = models.DateTimeField(
        verbose_name='만료일',
    )
    object_pks = models.JSONField(
        verbose_name='객체 pks',
        blank=True,
    )

    @property
    def is_expired(self):
        return self.expired_at < now() 
