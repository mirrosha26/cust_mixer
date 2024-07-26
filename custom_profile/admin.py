from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User

class CustomUserAdmin(BaseUserAdmin):
    model = User

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'uuid', 'domain')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Additional info'), {'fields': ('is_connected', 'order_id', 'body_html', 'head_html')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_connected'),
        }),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'uuid', 'is_connected', 'order_id')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'is_connected')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

admin.site.register(User, CustomUserAdmin)
