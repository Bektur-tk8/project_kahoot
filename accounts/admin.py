
from accounts.models import User, Point, Rating
from django.contrib import admin

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "last_name",
        "group",
        "phone",
        "email",
        "rating_place",
        "score"
    ]
    search_fields = [
        "first_name",
        "last_name",
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
    list_display = ['email', 'name', 'second_name', 'group',
                    'phone', 'score', 'rating_place',
                    'get_passed_tests']
    list_filter = ['group']
    search_fields = ['name', 'second_name', 'phone']


    def get_passed_tests(self, obj):
        return obj.test_participants.filter(completed=True).count()
