from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

class UserAdmin(admin.ModelAdmin):
    inlines = (ProfileInline,)

# Удаление стандартного UserAdmin и регистрация своего
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
