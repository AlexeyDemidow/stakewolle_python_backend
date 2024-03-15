from django.contrib import admin
from .models import Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class AdminUser(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    add_fieldsets = ((None, {'fields': ('id', 'username', 'email', 'password1', 'password2'), 'classes': ('wide',)}),)


class ProfileAdmin(admin.ModelAdmin):
    """Модель пользователя в админ-панели"""

    class Meta:
        model = Profile

    list_display = ['user', 'id', 'ref_code', 'expiration_date', 'ref_by']


admin.site.unregister(User)
admin.site.register(User, AdminUser)
admin.site.register(Profile, ProfileAdmin)
