from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
from django.utils.timezone import now
from django.utils.crypto import get_random_string

def unique_filename(instance, filename):
    base, extension = os.path.splitext(filename)
    user_id = instance.user.id
    timestamp = now().strftime('%Y%m%d%H%M%S')
    random_str = get_random_string(length=8)
    new_filename = f"{user_id}_{timestamp}_{random_str}{extension}"
    return os.path.join('backgrounds', new_filename)

def unique_filename_b(instance, filename):
    base, extension = os.path.splitext(filename)
    user_id = instance.user.id
    timestamp = now().strftime('%Y%m%d%H%M%S')
    random_str = get_random_string(length=8)
    new_filename = f"{user_id}_{timestamp}_{random_str}{extension}"
    return os.path.join('baners', new_filename)



User = get_user_model()

BACKGROUND_OPTIONS = [
        ('background_image', 'Фоновое  изображение'),
        ('main_color', 'Цвет основного фона'),
    ]

LOGIN_BACKGROUND_OPTIONS = [
        ('login_background_image', 'Фоновое  изображение'),
        ('login_background_color', 'Заливка цветом'),
    ]

class ThemeSettings(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="theme_settings")
    menu_color = models.CharField(max_length=7, default="#292929")
    menu_text_color = models.CharField(max_length=7, default="#ffffff")

    is_back_course_page_enabled = models.BooleanField(default=True)
    
    menu_line_height = models.FloatField(default=1.5)
    menu_line_color = models.CharField(max_length=7, default="#000000")

    footer_line_height = models.FloatField(default=1.5)
    footer_line_color = models.CharField(max_length=7, default="#000000")

    course_line_height = models.FloatField(default=1.5)
    course_line_color = models.CharField(max_length=7, default="#000000")

    main_color = models.CharField(max_length=7, default="#ffffff")
    text_color = models.CharField(max_length=7, default="#000000")

    scroll_bar_size = models.IntegerField(default=4)
    scroll_bar_color = models.CharField(max_length=7, default="#D9D9D9")
    scroll_bar_round = models.FloatField(default=0.1)

    accent_color = models.CharField(max_length=7, default="#707070")
    unaccent_color = models.CharField(max_length=7, default="#ffffff")
    border_accent_color = models.CharField(max_length=7, default="#000000")

    card_back_color = models.CharField(max_length=7, default="#ffffff")
    card_border_width = models.FloatField(default=1)
    card_border_color = models.CharField(max_length=7, default="#000000")
    card_border_radius = models.FloatField(default=0.1)

    menu_course_color = models.CharField(max_length=7, default="#292929")

    video_border_color = models.CharField(max_length=7, default="#000000")
    video_border_radius = models.FloatField(default=0.1)
    video_border_width = models.FloatField(default=1)

    left_menu_text_color = models.CharField(max_length=7, default="#ededed")
    left_menu_select_text_color = models.CharField(max_length=7, default="#1f1f1f")

    progress_bar_color = models.CharField(max_length=7, default="#46D04C")
    progress_border_color = models.CharField(max_length=7, default="#ffffff")
    progress_border_radius = models.FloatField(default=0.1)

    menu_course_background_selected = models.CharField(max_length=7, default="#46D04C")
    menu_course_right_selected = models.CharField(max_length=7, default="#111111")

    card_image_border_radius = models.FloatField(default=0.1)
    card_image_border_width = models.FloatField(default=0)
    card_image_border_color = models.CharField(max_length=7, default="#111111")
    card_button_color = models.CharField(max_length=7, default="#46D04C")
    card_button_border_radius = models.FloatField(default=0.1)
    card_button_border_width = models.FloatField(default=1)
    card_button_border_color = models.CharField(max_length=7, default="#04db00")

    progress_card_bar_color = models.CharField(max_length=7, default="#04db00")
    progress_card_border_radius = models.FloatField(default=0.1)
    progress_card_border_color = models.CharField(max_length=7, default="#bababa")
    progress_card_border_width = models.FloatField(default=1)

    card_text_color_secondary = models.CharField(max_length=7, default="#858585")
    card_text_color_primary = models.CharField(max_length=7, default="#111111")
    card_button_color_primary = models.CharField(max_length=7, default="#ffffff")

    login_input_back_color = models.CharField(max_length=7, default="#ffffff")
    login_input_border_radius = models.FloatField(default=0.1)
    login_input_border_width = models.FloatField(default=1)
    login_input_border_color = models.CharField(max_length=7, default="#07DF2B")
    login_input_text_color = models.CharField(max_length=7, default="#000000")

    login_school_color = models.CharField(max_length=7, default="#000000")
    login_title_color = models.CharField(max_length=7, default="#000000")
    login_label_color = models.CharField(max_length=7, default="#000000")
    login_link_label_color = models.CharField(max_length=7, default="#000000")

    login_button_back_color = models.CharField(max_length=7, default="#000000")
    login_button_border_radius = models.FloatField(default=0.1)
    login_button_border_width = models.FloatField(default=1)
    login_button_border_color = models.CharField(max_length=7, default="#000000")
    login_button_text_color = models.CharField(max_length=7, default="#ffffff")
    login_background_color = models.CharField(max_length=7, default="#000000")

    login_card_back_color = models.CharField(max_length=7, default="#ffffff")
    login_card_border_width = models.FloatField(default=0.1)
    login_card_border_color = models.CharField(max_length=7, default="#000000")
    login_card_border_radius = models.FloatField(default=0.1)

    hr_active_color = models.CharField(max_length=7, default="#46D04C")

    nps_back_color = models.CharField(max_length=7, default="#000000")
    nps_border_width = models.FloatField(default=0.1)
    nps_border_color = models.CharField(max_length=7, default="#D9D9D9")
    nps_border_radius = models.FloatField(default=0.1)
    nps_text_color = models.CharField(max_length=7, default="#ffffff")


    form_border_width = models.FloatField(default=0.1)
    form_border_color = models.CharField(max_length=7, default="#D9D9D9")
    form_border_radius = models.FloatField(default=0.1)
    form_text_color = models.CharField(max_length=7, default="#ffffff")
    form_back_color = models.CharField(max_length=7, default="#ffffff")

    form_button_back_color = models.CharField(max_length=7, default="#111111")
    form_button_border_width = models.FloatField(default=0.1)
    form_button_border_color = models.CharField(max_length=7, default="#111111")
    form_button_border_radius = models.FloatField(default=0.1)
    form_button_text_color = models.CharField(max_length=7, default="#ffffff")

    form_button_back_default_color = models.CharField(max_length=7, default="#111111")
    form_button_border_default_width = models.FloatField(default=0.1)
    form_button_border_default_color = models.CharField(max_length=7, default="#111111")
    form_button_border_default_radius = models.FloatField(default=0.1)
    form_button_text_default_color = models.CharField(max_length=7, default="#ffffff")

    card_bage_text_color = models.CharField(max_length=7, default="#111111")
    card_bage_background_color = models.CharField(max_length=7, default="#ffffff")
    link_color = models.CharField(max_length=7, default="#3762ff")


    background_image = models.ImageField(
        upload_to=unique_filename,
        blank=True,
        null=True,
        default='backgrounds/default_background.png'
    )

    login_background_image = models.ImageField(
        upload_to=unique_filename,
        blank=True,
        null=True,
        default='backgrounds/default_background.png'
    )

    background_option = models.CharField(
        max_length=20,
        choices=BACKGROUND_OPTIONS,
        default='main_color',
    )

    login_background_option = models.CharField(
        max_length=30,
        choices=LOGIN_BACKGROUND_OPTIONS,
        default='login_background_color',
    )

    baner_image = models.ImageField(
        upload_to=unique_filename_b,
        default='baners/default_baner.png',
    )

    baner_mob_image = models.ImageField(
        upload_to=unique_filename_b,
        default='baners/default_baner.png',
    )

    banner_url = models.URLField(max_length=200, default='')


    telegram_url = models.URLField(default='', blank=True, verbose_name="Ссылка на Телеграм")
    instagram_url = models.URLField(default='', blank=True, verbose_name="Ссылка на Инстаграм")
    vk_url = models.URLField(default='', blank=True, verbose_name="Ссылка на ВК")
    x_url = models.URLField(default='', blank=True, verbose_name="Ссылка на X (Twitter)")
    youtube_url = models.URLField(default='', blank=True, verbose_name="Ссылка на YouTube")
    whatsapp_url = models.URLField(max_length=255, blank=True, default='')




    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) 
        if self.background_image:
            os.chmod(self.background_image.path, 0o644)
        if self.login_background_image:
            os.chmod(self.login_background_image.path, 0o644)

    


    def __str__(self):
        return f"{self.user.username}'s Theme Settings"

@receiver(post_save, sender=User)
def create_theme_settings(sender, instance, created, **kwargs):
    if created:
        ThemeSettings.objects.create(user=instance)





def reset_fields_to_default(instance, field_names):
    """
    Сбрасывает значения указанных полей на значения по умолчанию.
    Если возникает исключение, то поле пропускается.

    :param instance: Экземпляр модели ThemeSettings
    :param field_names: Список названий полей, которые нужно сбросить
    """
    for field_name in field_names:
        try:
            if not hasattr(instance, field_name):
                print(f"Поле '{field_name}' не существует в модели '{instance.__class__.__name__}'. Пропуск...")
                continue

            field = instance._meta.get_field(field_name)
            
            if field.default == models.fields.NOT_PROVIDED:
                print(f"Поле '{field_name}' не имеет значения по умолчанию. Пропуск...")
                continue

            # Устанавливаем значение по умолчанию
            setattr(instance, field_name, field.default)

        except Exception as e:
            # Можно логировать исключение или просто пропустить
            print(f"Ошибка при сбросе поля '{field_name}': {e}. Пропуск...")

    # Сохраняем изменения только один раз после установки всех значений
    instance.save()