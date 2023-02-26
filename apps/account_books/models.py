from core.models import BaseModel
from django.contrib.auth import get_user_model
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models


class AccountBook(BaseModel):
    user = models.ForeignKey(
        verbose_name='유저',
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name='account_books',
    )
    name = models.CharField(
        verbose_name='이름',
        max_length=20,
        validators=[
            MinLengthValidator(3),
        ]
    )
