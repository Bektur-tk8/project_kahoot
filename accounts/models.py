from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models

from group.models import UserGroup

from quiz.models import Quiz, Question

class UserManager(BaseUserManager):
    def _create(self, email, password, name, **fields):
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, name, **fields):
        fields.setdefault('is_active', True)
        fields.setdefault('is_staff', False)
        return self._create(email, password, name, **fields)

    def create_superuser(self, email, password, name, **fields):
        fields.setdefault('is_active', True)
        fields.setdefault('is_staff', True)
        return self._create(email, password, name, **fields)

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
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    objects = UserManager()

    class Meta:
        ordering = ["rating_place"]



