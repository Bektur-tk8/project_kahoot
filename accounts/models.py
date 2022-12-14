from operator import truediv
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models

from group.models import UserGroup

from quiz.models import Quiz, Question

class UserManager(BaseUserManager):

    def create_user(self, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username=None
    name = models.CharField(max_length=65)
    second_name = models.CharField(max_length=65)
    email = models.EmailField("Email", unique=True)
    phone = models.CharField(
        'Номер телефона',
        null=True,
        max_length=10
    )
    group = models.ForeignKey(UserGroup, on_delete=models.SET_NULL, null=True)
    score = models.BigIntegerField("Итоговый балл", blank=True, default=0)
    rating_place = models.IntegerField("Место в рейтинге", blank=True, default=0)
    group_rating = models.IntegerField("group_rating", default=0)
    # past_test_count = models.IntegerField("Количество пройденных тестов", default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    objects = UserManager()

    class Meta:
        ordering = ["rating_place"]