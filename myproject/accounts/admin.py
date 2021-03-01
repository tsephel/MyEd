from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile
from .forms import UpdateUserForm, AddUserForm

#Here we register all the models for account app which we have created so that it is displayed in admin page
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass

class UserAdmin(BaseUserAdmin):
    form = UpdateUserForm
    add_form = AddUserForm

    list_display = ('email', 'full_name')
    list_filter = ( 'groups', )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name',)}),
        ('Permissions', {'fields': ( 'groups',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email', 'full_name', 'password1',
                    'password2',
                )
            }
        ),
    )
    search_fields = ('email', 'full_name')
    ordering = ('email', 'full_name')
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
