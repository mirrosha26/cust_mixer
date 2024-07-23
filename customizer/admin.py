from django.contrib import admin
from .models import ThemeSettings

class ThemeSettingsAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'menu_color', 'menu_text_color', 'menu_line_height', 'menu_line_color',
        'main_color', 'text_color', 'scroll_bar_size', 'scroll_bar_color', 'scroll_bar_round',
        'accent_color', 'unaccent_color', 'border_accent_color', 'card_back_color',
        'card_border_width', 'card_border_color', 'menu_course_color', 'background_image',
        'background_option'
    ]
    search_fields = ['user__username']
    list_filter = ['menu_color', 'text_color', 'accent_color']
    ordering = ['user']

admin.site.register(ThemeSettings, ThemeSettingsAdmin)