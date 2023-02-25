from core.models import BaseModel
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(BaseModel, AbstractUser):
    username = None
    email = models.EmailField(
        verbose_name='이메일',
        unique=True,
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
