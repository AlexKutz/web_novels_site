from django.contrib import admin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User

from django.contrib.auth.admin import UserAdmin

from novel.models import UserBookShelfBook


class UserBookShelfInline(admin.TabularInline):
    model = UserBookShelfBook
    fields = ['novel', ]
    readonly_fields = ['added', ]


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    inlines = [UserBookShelfInline, ]
    list_display = ('username', 'email', 'is_staff', 'is_active',)
    list_filter = ('username', 'email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'image', 'email', 'is_active_email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'image', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)


admin.site.register(User, CustomUserAdmin)