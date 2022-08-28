from accounts.models import User
from django.contrib import admin

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "second_name",
        "group",
        "phone",
        'email',
        "rating_place",
        "score"
    ]
    exclude = ["first_name", "last_name", "groups", "last_login", 
    "superuser_status", "user_permissions", "date_joined", "group_rating"]
    search_fields = [
        "name",
        "second_name",
        "phone",
    ]
    list_filter = [
        "group"
    ]


class UserAdminProxy(User):
    class Meta:
        proxy = True
        verbose_name = 'LeadersTable'
        verbose_name_plural = 'LeadersTable'


@admin.register(UserAdminProxy)
class LeaderBoard(admin.ModelAdmin):
    list_display = ['name', 'second_name', 'group',
                    'phone', 'email', 'score', 'rating_place',
                    'passed_tests']
    exclude = ["groups", "last_login", "first_name", "last_name", 
    "superuserstatus", "user_permissions", "date_joined", "group_rating"]
    list_filter = ['group']
    search_fields = ['name', 'second_name', 'phone']


    def passed_tests(self, obj):
        return obj.quiz_takers.filter(completed=True).count()