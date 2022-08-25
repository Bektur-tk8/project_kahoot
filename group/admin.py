from email.headerregistry import Group
import imp
from django.contrib import admin

# Register your models here.
from group.models import UserGroup

@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    model = UserGroup
    list_display = ['name']
    