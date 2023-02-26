from core.models import BaseModel
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MinValueValidator
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


class Transaction(BaseModel):
    account_book = models.ForeignKey(
        verbose_name='가계부',
        to=AccountBook,
        on_delete=models.CASCADE,
        related_name='transactions',
    )
    description = models.TextField(
        verbose_name='설명',
    )
    occurred_at = models.DateTimeField(
        verbose_name='발생일',
    )
    amount = models.PositiveIntegerField(
        verbose_name='금액',
        validators=[
            MinValueValidator(1),
        ]
    )
    type = models.CharField(
        verbose_name='거래 유형',
        max_length=1,
        choices=[
            ('+', '수입'),
            ('-', '지출'),
        ]
    )
