from django.contrib import admin
import nested_admin
from .models import *


class AnswerInLine(nested_admin.NestedStackedInline):
    model = Answer
    extra = 4
    max_num = 4

    def has_delete_permission(self, request, obj=None):
        return False



class QuestionInLine(nested_admin.NestedStackedInline):
    model = Question
    inlines = [AnswerInLine,]
    extra = 5


class QuizAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInLine,]

class UsersAnswerInLine(admin.StackedInline):
    model = UsersAnswer

class QuizTakerAdmin(admin.ModelAdmin):
    inlines = [UsersAnswerInLine, ]

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(QuizTaker, QuizTakerAdmin)
admin.site.register(UsersAnswer)



