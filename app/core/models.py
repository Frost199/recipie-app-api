"""
Core Model For User Manager
"""
# inbuilt libraries

from typing import Dict

# third party library
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager,
                                        PermissionsMixin)


# custom imports
# from app.libs.strings import get_text


class UserManager(BaseUserManager):
    """
    User manager class
    """

    def create_user(self, email: str, password: str = None,
                    **extra_fields: Dict):
        """
        Creates and save a new user
        Args:
            email: email address of a user
            password: password field for a user, can be none
            **extra_fields: extra fields for a given user

        Returns:

        """
        if not email:
            # raise ValueError(get_text("user_no_email"))
            raise ValueError("User must have an email address")
        user = self.model(email=self.normalize_email(email),
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str):
        """
        Creates and saves a new super user
        Args:
            email: email of super user
            password: password of superuser

        Returns:

        """
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that supports email instead of username
    """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
