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
    # past_test_count = models.IntegerField("Количество пройденных тестов", default=0)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    

# class LeaderBoard(models.Model):
#     name = models.CharField(max_length=65)
#     second_name = models.CharField(max_length=65)
#     group = models.ForeignKey(UserGroup, on_delete=models.SET_NULL, null=True)
#     phone = models.CharField(
#         'Номер телефона',
#         null=True,
#         max_length=10
#     )
#     email = models.EmailField("Email", unique=True)
#     rating_place = models.IntegerField("Место в рейтинге", blank=True, default=0)
#     score = models.BigIntegerField("Итоговый балл", blank=True, default=0)
#     past_test_count = models.IntegerField("Количество пройденных тестов", default=0)
#     is_active = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    objects = UserManager()

    class Meta:
        ordering = ["rating_place"]



class Point(models.Model):
    login = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.SmallIntegerField()
    test = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.login)


class Rating(models.Model):
    login = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField()
    test = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.login)


class QuestionTime(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    test = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    time = models.CharField(max_length=100)


class QuestionScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    test = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.SmallIntegerField(blank=True)
    answer = models.CharField(max_length=100)