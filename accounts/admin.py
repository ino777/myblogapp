""" Account admin settings """
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _


from .models import User


# Register your models here.
class MyUserChangeForm(UserChangeForm):
    """ User settings change form """
    class Meta:
        model = User
        fields = '__all__'


class MyUserCreationForm(UserCreationForm):
    """ User creation form """
    class Meta:
        model = User
        fields = ('email',)


class MyUserAdmin(UserAdmin):
    """ ModelAdmin for User """
    fieldsets = (
        (None, {'fields': ('id', 'email', 'password')}),
        (_('Personal info'), {
            'fields': ('username', 'icon_image', 'profile_message', 'first_name', 'last_name', 'birth_date')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'reg_date')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('id',)

    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ('username', 'email', 'reg_date', 'last_login', 'is_active', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'username')
    ordering = ('email',)


admin.site.register(User, MyUserAdmin)
