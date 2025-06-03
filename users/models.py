from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .usermanager import UserManager
from django.utils import timezone


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('instructor', 'instructor'),
        ('client', 'client'),
    )
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'role']

    def __str__(self):
        return f"{self.name} ({self.role})"

