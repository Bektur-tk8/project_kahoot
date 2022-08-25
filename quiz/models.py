from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify

from group.models import UserGroup


class Quiz(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=70, blank=True)
    image = models.ImageField()
    group = models.ForeignKey(UserGroup, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=False)


    def __str__(self):
        return str(self.name)


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    question = models.TextField()
    image = models.ImageField(blank=True)
    score = models.SmallIntegerField(default=100)
    timer = models.SmallIntegerField(default=20)
	

    def __str__(self):
	    return self.question


class Answer(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
	label = models.CharField(max_length=100)
	is_correct = models.BooleanField(default=False)

	def __str__(self):
		return self.label


class TestParticipant(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, 
    on_delete=models.CASCADE, related_name="test_participants")
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="completed_tests")
	score = models.IntegerField(default=0)
	completed = models.BooleanField(default=False)
	date_finished = models.DateTimeField(null=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.user.email


class UsersAnswer(models.Model):
	test_participant = models.ForeignKey(TestParticipant, on_delete=models.CASCADE, related_name="user_answers")
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True)

	def __str__(self):
		return str(self.question.id)


# @receiver(pre_save, sender=Quiz)
# def slugify_name(sender, instance, *args, **kwargs):
# 	instance.slug = slugify(instance.name)