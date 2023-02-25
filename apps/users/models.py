from core.models import BaseModel
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password):
        user = self.model(email=email)
        user.set_password(password)
        user.save()
        return user


class User(BaseModel, AbstractUser):
    username = None
    email = models.EmailField(
        verbose_name='이메일',
        unique=True,
    )

    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
