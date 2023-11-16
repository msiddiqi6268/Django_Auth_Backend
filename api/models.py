from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import re

class UserAccountManager(BaseUserManager):
    def create_user(self, email,username, password=None, **extra_fields):
        regex = r"^[a-zA-Z0-9_]+(?:[a-zA-Z0-9_]+)*$"
        if not email:
            raise ValueError('Users must have an email address')

        if not username:
            raise ValueError("Users must have an username")
        elif not re.match(regex, username) is not None:
            raise ValueError("Username is invalid")

        email = self.normalize_email(email)
        username = username.lower()
        user = self.model(email=email, username=username, **extra_fields)

        user.set_password(password)
        user.save()

        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    phone = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone']

    def __str__(self):
        return self.email