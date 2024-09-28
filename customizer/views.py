from django.shortcuts import render, get_object_or_404, redirect
from .utils import Shape, Circle, Text, Image, CustomElement
from .factories import text_factory, circle_factory, shape_factory, image_factory, custom_element_factory
from django.views import View
from .models import ThemeSettings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import BACKGROUND_OPTIONS, LOGIN_BACKGROUND_OPTIONS, reset_fields_to_default


# Пример использования
# theme_settings_instance = ThemeSettings.objects.get(id=1)  # Получите экземпляр модели
# reset_fields_to_default(theme_settings_instance, ['menu_color', 'text_color', 'main_color'])  # Сброс значений нескольких полей


@login_required
def reset_theme_settings(request):
    if request.method == 'POST':
        fields_to_reset = request.POST.get('fields_to_reset', '')
        fields_to_reset_list = [field.strip() for field in fields_to_reset.split(',')]        
        theme_settings = ThemeSettings.objects.get(user=request.user)        
        reset_fields_to_default(theme_settings, fields_to_reset_list)
        referer_url = request.META.get('HTTP_REFERER', 'default_view_name')
    return redirect(referer_url)


def create_card_elements(ts, base_x=0, base_y=0):
    """
    Создает список элементов для карточки курса с использованием настроек темы.

    :param ts: объект ThemeSettings, содержащий стилевые настройки.
    :param base_x: базовая координата X для всех элементов.
    :param base_y: базовая координата Y для всех элементов.
    :return: список элементов карточки.
    """
    card_elements = [
        shape_factory(
            145, 180, ts.card_back_color, base_x + 0, base_y + 0, "None",
            border_radius=ts.card_border_radius, 
            border_width=ts.card_border_width, 
            border_color=ts.card_border_color
        ),
        shape_factory(
            124, 50, "#7ee4d7", base_x + 11, base_y + 11, "None",
            border_radius=ts.card_image_border_radius, 
            border_width=ts.card_image_border_width, 
            border_color=ts.card_image_border_color
        ),
        shape_factory(
            124, 20, ts.card_button_color, base_x + 11, base_y + 145, "None",
            border_radius=ts.card_button_border_radius, 
            border_width=ts.card_button_border_width, 
            border_color=ts.card_button_border_color
        ),
        shape_factory(
            100, 4, ts.card_back_color, base_x + 13, base_y + 135, "None",
            border_radius=ts.progress_card_border_radius, 
            border_width=1, 
            border_color=ts.progress_card_border_color
        ),
        shape_factory(
            70, 2.4, ts.progress_card_bar_color, base_x + 13.2, base_y + 136.1, "None",
            border_radius=0
        ),
        text_factory(
            base_x + 120, base_y + 135, "None", "70%", 6, ts.card_text_color_secondary, 6
        ),
        text_factory(
            base_x + 13, base_y + 119, "None", "Описание курса", 7, ts.card_text_color_secondary, 7),

        text_factory(
            base_x + 13, base_y + 68, "None", "Название курса", 9, ts.card_text_color_primary, 9
        ),
        text_factory(
            base_x + 45, base_y + 152, "None", "ПРОДОЛЖИТЬ", 7, ts.card_button_color_primary, 7
        )
    ]
    return card_elements

class MainCustomizerView(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('signin') 
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        emulator_size = {'width': 700, 'height': 560 }
        ts = ThemeSettings.objects.get(user=request.user)

        if ts.background_option == "background_image":
            background_image = ts.background_image
        else:
            background_image = ""
        # Заливки
        el_menu_background = shape_factory(emulator_size['width'], 32, ts.menu_color, 0, 0, "el_menu_background")
        el_main_background = shape_factory(emulator_size['width'], 460, ts.main_color, 0, 32, "el_main_background",  background_image=background_image)

        el_menu_line = shape_factory(emulator_size['width'], round(ts.menu_line_height / 1.5, 1), ts.menu_line_color, 0, 32, "el_menu_line")
        el_scroll_bar = shape_factory(round(ts.scroll_bar_size / 1.5, 1), 220, ts.scroll_bar_color, emulator_size['width'] - round(ts.scroll_bar_size / 1.5, 1), 50, "el_scroll_bar", border_radius=ts.scroll_bar_round)
        
        #Аватарка
        el_avatar = circle_factory(22, ts.accent_color, 593, 4, "el_avatar")
        el_avatar_text = text_factory(597, 11, "el_avatar_text", "MA", 9, ts.unaccent_color, 9)


        el_icon1 = circle_factory(17, f"{ts.accent_color}", 545, 7, "el_avatar")
        el_icon2 = circle_factory(17, f"{ts.accent_color}", 569, 7, "el_avatar")

        el_logo = shape_factory(22, 22, "#858585", 12, 4, "el_logo", border_radius=0.2)
        el_nav1 = text_factory(45, 11, "el_menu_text_nav", "Курсы и материалы", 8, ts.menu_text_color ,8, "bold")
        el_nav2 = text_factory(135, 11, "el_menu_text_nav", "Форум", 8, ts.menu_text_color ,8)
        el_nav3 = text_factory(175, 11, "el_menu_text_nav", "Доступы и оплаты", 8, ts.menu_text_color ,8)
        el_nav4 = text_factory(260, 11, "el_menu_text_nav", "Партнерская программа", 8, ts.menu_text_color ,8)
        el_nav5 = text_factory(623, 12, "el_menu_text_nav", "Имя пользователя", 7, ts.menu_text_color ,7)

        

        el_dropdown = shape_factory(72, 14, "#fafafa", 615, 47, "el_dropdown", border_radius=0.1, border_color=ts.border_accent_color, border_width=0.2)
        el_search = shape_factory(118, 14, "ffffff90", 499, 47, "el_search", border_radius=0.1, border_width=0.1, border_color=ts.border_accent_color)
        el_h1 = text_factory(12, 46, "el_h1", "Курсы", 14, ts.text_color, 14)
    
        # Создание элементов для каждой карточки с различными координатами
        card1 = create_card_elements(ts, base_x=12, base_y=78)
        card2 = create_card_elements(ts, base_x=166, base_y=78)
        card3 = create_card_elements(ts, base_x=321, base_y=78)
        card4 = create_card_elements(ts, base_x=476, base_y=78)
        card5 = create_card_elements(ts, base_x=12, base_y=267)
        card6 = create_card_elements(ts, base_x=166, base_y=267)

        # Объединение всех элементов в один список
        cards = card1 + card2 + card3 + card4 + card5 + card6
        sorted_options = [opt for opt in BACKGROUND_OPTIONS if opt[0] == ts.background_option]
        sorted_options += [opt for opt in BACKGROUND_OPTIONS if opt[0] != ts.background_option]

        if ts.background_image == 'backgrounds/default_background.png':
            reset = 'true'
        else:
            reset = 'false'

        # Контекст для передачи в шаблон
        context = {
            'title': 'Основные настройки страницы курсов',
            'device_browser_header' : True,
            'base_layer': [el_menu_background, el_main_background],
            'content_layer': [el_menu_line, el_nav1, el_nav2, el_nav3, el_nav4, el_nav5, el_avatar, el_icon1, el_icon2, el_h1,  el_search],
            'overlay_layer': [el_dropdown, el_avatar_text],
            'top_layer': [el_scroll_bar, el_logo] + cards,
            'emulator_size': emulator_size,
            'blocks': [
                {
                    'name': 'Меню',
                    'inputs': [
                        {'label': 'Фон меню', 'type': 'backgroundColor', 'name': 'menu_color', 'value': ts.menu_color, 'elements': ['el_menu_background'] },
                        {'label': 'Цвет текста меню', 'type': 'color', 'name': 'menu_text_color', 'value': ts.menu_text_color, 'elements': ['el_menu_text_nav']  }
                    ]
                },
                {
                    'name': 'Линия под меню',
                    'inputs': [
                        {'label': 'Цвет линии под меню', 'type': 'backgroundColor', 'name': 'menu_line_color', 'value': ts.menu_line_color, 'elements': ['el_menu_line']  },
                        {'label': 'Толщина линии под меню (px)', 'type': 'lineHeight', 'name': 'menu_line_height', 'value': ts.menu_line_height, 'elements': ['el_menu_line']  },
                    ]
                },
                {
                    'name': 'Базовые цвета',
                    'inputs': [
                        {'label': 'Основной фон (используется на всем сайте)', 'type': 'backgroundColor', 'name': 'main_color', 'value': ts.main_color, 'elements': ['el_main_background']  },
                        {'label': 'Вариант оформления фона курса', 'type': 'select', 'name': 'background_option', 'options': sorted_options, 'elements': ['select']  },
                        {'label': 'Фоновое изображение', 'type': 'img', 'name': 'background_image', 'value': ts.background_image, 'elements': ['el_main_background']  },
                        {'label': 'Цвет текста', 'type': 'color', 'name': 'text_color', 'value': ts.text_color, 'elements': ['el_h1']  },
                    ]
                },
                {
                    'name': 'Акцентные цвета',
                    'inputs': [
                        {'label': 'Акцентный цвет (заливка)', 'type': 'backgroundColor', 'name': 'accent_color', 'value': ts.accent_color, 'elements': ['el_avatar']  },
                        {'label': 'Цвет текста на акцентой заливке', 'type': 'color', 'name': 'unaccent_color', 'value': ts.unaccent_color, 'elements': ['el_avatar_text']  },
                    ]
                },
                {
                    'name': 'Полоса прокрутки (scroll bar)',
                    'inputs': [
                        {'label': 'Цвет полосы прокрутки', 'type': 'backgroundColor', 'name': 'scroll_bar_color', 'value': ts.scroll_bar_color, 'elements': ['el_scroll_bar']  },
                    ]
                },
                {
                    'name': 'Обводка',
                    'inputs': [
                        {'label': 'Цвет обводки (для всех элементов на сайте с обводкой)', 'type': 'borderColor', 'name': 'border_accent_color', 'value': ts.border_accent_color, 'elements': ['el_search', 'el_dropdown'] },
                    ]
                },
            ],
            "reset" : reset
        }
        return render(request, 'customizer/customizer.html', context)

    def post(self, request):
        ts = ThemeSettings.objects.get(user=request.user)

        # Обновляем значения других полей из POST данных
        for key, value in request.POST.items():
            if value == '.' or value == '':
                continue
            if hasattr(ts, key) and key != 'background_image':
                setattr(ts, key, value)


        # Проверяем и обрабатываем файл, если он существует
        if 'background_image' in request.FILES and request.FILES['background_image'].size > 0:
            ts.background_image = request.FILES['background_image']
        else:
            # Если файл не был загружен или пуст, не изменяем поле background_image
            pass
        
        # Проверяем значение reset и обновляем поле если необходимо
        reset = request.POST.get('reset', 'false')
        if reset == 'true':
            # Устанавливаем изображение по умолчанию из папки media
            default_image_path = 'backgrounds/default_background.png'
            ts.background_image = default_image_path
        
        # Сохраняем изменения в базе данных
        ts.save()
        
        # Перенаправляем пользователя на нужную страницу
        return redirect('custom_main')


class LessonCustomizerView(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('signin') 
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        emulator_size = {'width': 700, 'height': 400 }
        ts = ThemeSettings.objects.get(user=request.user)

        el_menu_background = shape_factory(530, 32, ts.menu_color, 170, 0, "el_menu_background")
        el_main_background = shape_factory(530, 368, ts.main_color, 170, 32, "el_main_background")
        el_course_background = shape_factory(170, 400, ts.menu_course_color, 0, 0, "el_course_background") #настройка [+]
        
        el_menu_line = shape_factory(530, round(ts.menu_line_height / 1.5, 1), ts.menu_line_color, 170, 32, "el_menu_line") 
        el_scroll_bar = shape_factory(round(ts.scroll_bar_size / 1.5, 1), 220, ts.scroll_bar_color, emulator_size['width'] - round(ts.scroll_bar_size / 1.5, 1), 50, "el_scroll_bar", border_radius=ts.scroll_bar_round)

        el_avatar = circle_factory(22, ts.accent_color, 593, 4, "el_avatar")
        el_avatar_text = text_factory(597, 11, "el_avatar_text", "MA", 9, ts.unaccent_color, 9)

        el_icon1 = circle_factory(17, f"{ts.accent_color}", 545, 7, "el_avatar")
        el_icon2 = circle_factory(17, f"{ts.accent_color}", 569, 7, "el_avatar")
        el_nav5 = text_factory(623, 12, "el_menu_text_nav", "Имя пользователя", 7, ts.menu_text_color ,7)

        el_nav1 = text_factory(186, 11, "el_menu_text_nav", "Курс >  Раздел курса", 8, ts.menu_text_color ,8)

        el_video_border = shape_factory(435, 240, "ffffff00", 215, 55, "el_video_border", ts.video_border_radius , ts.video_border_width, ts.video_border_color)  #настройка [+]
        video_image = image_factory(left=220, top=60, class_id="video_image", image_name="video_image.png") 

        #Левое  меню
        el_ltext_nav1 = text_factory(10, 11, "el_lmenu_text", "< Назад к курсам", 8, ts.left_menu_text_color ,8)
        el_ltext_nav2 = text_factory(8, 29, "el_lmenu_text", "Курс", 10, ts.left_menu_text_color ,10, "medium")
        
        el_ltext_nav3 = text_factory(9, 57, "el_lmenu_text", "Шаг 1 из 2", 6, ts.left_menu_text_color ,6)
        
        el_ltext_nav4 = text_factory(142, 57, "el_lmenu_text", "100%", 6, ts.left_menu_text_color ,6)
        el_ltext_nav5 = text_factory(8, 82, "el_lmenu_text", "[ ] Поиск", 7, ts.left_menu_text_color ,7)

        el_ltext_nav6 = shape_factory(6, 6, f"{ts.left_menu_text_color}", 9, 109, "el_lmenu_text", border_radius=0.1)
        el_ltext_nav7 = text_factory(19, 110, "el_lmenu_text", "Бонусы от Техно Гуру", 7, ts.left_menu_text_color ,7, "bold")
        el_ltext_nav8 = text_factory(23, 137, "el_lmenu_select_text", "Воркшоп по Miro", 7, ts.left_menu_select_text_color ,7, "bold")
        el_ltext_nav9 = text_factory(23, 162, "el_lmenu_text", "Воркшоп по Figma", 7, ts.left_menu_text_color ,7, "bold")

        el_divider = shape_factory(153, 0.4, f"{ts.left_menu_text_color}", 8, 70, "el_lmenu_text", border_radius=0.1)  #настройка [+]
        el_progress_bar_back = shape_factory(153, 5, ts.menu_course_color, 8, 47.5, "el_progress_back", ts.progress_border_radius, 1, ts.progress_border_color)  #настройка [+]
        el_progress = shape_factory(133, 4, ts.progress_bar_color, 8.5, 48, "el_progress", border_radius=0.1)  #настройка [+]

        el_corse_menu_background_selected = shape_factory(169, 21, ts.menu_course_background_selected , 0, 130, "el_corse_menu_background_selected")  #настройка [+]
        el_courese_menu_indicator1 = circle_factory(4, f"{ts.left_menu_text_color}", 156, 111, "el_lmenu_text")
        el_courese_menu_indicator2 = circle_factory(4, f"{ts.left_menu_select_text_color}", 156, 139, "el_courese_menu_indicator2")
        el_course_line = shape_factory(round(ts.course_line_height / 1.5, 1), 400, ts.course_line_color, 170, 0, "el_course_line")
        
        el_course_menu_active = shape_factory( 2, 21, ts.menu_course_right_selected , 168, 130, "el_menu_course_right_selected", border_radius=0)  #настройка [+]
        video_border = shape_factory(435, 240, "ffffff00", 215, 55, "el_video_border", ts.video_border_radius , ts.video_border_width, ts.video_border_color)  

        el_form_button = shape_factory(60, 21, ts.form_button_back_color , 635, 372, "el_form_button", border_radius=ts.form_button_border_radius, border_width=ts.form_button_border_width, border_color=ts.form_button_border_color)
        el_form_button_text = text_factory(644, 377, "el_form_button_text", 'ВПЕРЕД <i class="bi-arrow-right"></i>', 8, ts.form_button_text_color)

        el_form_button_start = shape_factory(60, 21, ts.form_button_back_default_color , 181, 372, "el_form_button_start", border_radius=ts.form_button_border_default_radius, border_width=ts.form_button_border_default_width, border_color=ts.form_button_border_default_color)
        el_form_button_text_start = text_factory(189, 377, "el_form_button_text_start", '<i class="bi-arrow-left"></i> НАЗАД', 8, ts.form_button_text_default_color)

        el_footer_line = shape_factory(530, round(ts.footer_line_height / 1.5, 1), ts.footer_line_color, 170, 364, "el_footer_line") 

        context = {
            'title': 'Настройка страницы курса',
            'device_browser_header' : True,
            'base_layer': [el_course_background, el_menu_background, el_main_background],
            'content_layer': [el_menu_line, el_icon1, el_icon2, el_avatar, el_nav1, el_nav5, el_video_border, 
                el_ltext_nav1, el_ltext_nav2, el_ltext_nav3, el_ltext_nav4, el_ltext_nav5, el_ltext_nav6,
                el_ltext_nav7, el_ltext_nav9, el_divider, el_progress_bar_back,
                el_corse_menu_background_selected],
            'overlay_layer': [el_avatar_text, video_image, el_progress, el_ltext_nav8, el_courese_menu_indicator1, 
                                el_courese_menu_indicator2, el_footer_line, el_course_menu_active, el_form_button, el_form_button_start],
            'top_layer': [el_scroll_bar, el_form_button_text, el_form_button_text_start, el_course_line],
            'emulator_size': emulator_size,
            'blocks': [
                {
                    'name': 'Фон и текст контента',
                    'inputs': [
                        {'label': 'Использовать основной фон и цвет текста из настроек "Курсы". Если опция отключена, фон и текст нужно будет настроить отдельно для каждого урока в AXL', 'type': 'checkbox', 'name': 'is_back_course_page_enabled', 'value': ts.is_back_course_page_enabled },
                    ],
                },
                {
                    'name': 'Боковое меню',
                    'inputs': [
                        {'label': 'Фон', 'type': 'backgroundColor', 'name': 'menu_course_color', 'value': ts.menu_course_color, 'elements': ['el_course_background'] },
                        {'label': 'Цвет текста бокового меню', 'type': 'color', 'name': 'left_menu_text_color', 'value': ts.left_menu_text_color, 'elements': ['el_lmenu_text']  }
                    ],
                },
                {
                    'name': 'Активный этап в меню курса',
                    'inputs': [
                        {'label': 'Фон активной вкладки', 'type': 'backgroundColor', 'name': 'menu_course_background_selected', 'value': ts.menu_course_background_selected, 'elements': ['el_corse_menu_background_selected'] },
                        {'label': 'Цвет бокового бордюра вкладки', 'type': 'backgroundColor', 'name': 'menu_course_right_selected', 'value': ts.menu_course_right_selected, 'elements': ['el_menu_course_right_selected'] },
                        {'label': 'Цвет текста активной вкладки', 'type': 'color', 'name': 'left_menu_select_text_color', 'value': ts.left_menu_select_text_color, 'elements': ['el_lmenu_select_text', 'el_courese_menu_indicator2']  }
                    ],
                },
                {
                    'name': 'Прогресс-бар',
                    'inputs': [
                        {'label': 'Цвет', 'type': 'backgroundColor', 'name': 'progress_bar_color', 'value': ts.progress_bar_color, 'elements': ['el_progress'] },
                        {'label': 'Цвет обводки', 'type': 'borderColor', 'name': 'progress_border_color', 'value': ts.progress_border_color, 'elements': ['el_progress_back'] },
                        {'label': 'Радиус скругленя обводки', 'type': 'borderRadius', 'name': 'progress_border_radius', 'value': ts.progress_border_radius, 'elements': ['el_progress_back']},
                    ],
                },
                {
                    'name': 'Обводка  видео',
                    'inputs': [
                        {'label': 'Цвет', 'type': 'borderColor', 'name': 'video_border_color', 'value': ts.video_border_color, 'elements': ['el_video_border'] },
                        {'label': 'Толщина линии обводки', 'type': 'borderWidth', 'name': 'video_border_width', 'value': ts.video_border_width, 'elements': ['el_video_border']  },      
                        {'label': 'Радиус скругленя обводки', 'type': 'borderRadius', 'name': 'video_border_radius', 'value': ts.video_border_radius, 'elements': ['el_video_border']  },             
                    ],
                },
                {
                    'name': 'Стиль основных кнопок (В примере кнопка "ВПЕРЕД")',
                    'inputs': [
                        {'label': 'Цвет кнопки', 'type': 'backgroundColor', 'name': 'form_button_back_color', 'value': ts.form_button_back_color, 'elements': ['el_form_button']},
                        {'label': 'Цвет текста кнопки', 'type': 'color', 'name': 'form_button_text_color', 'value': ts.form_button_text_color, 'elements': ['el_form_button_text']},
                        {'label': 'Цвет обводки кнопки', 'type': 'borderColor', 'name': 'form_button_border_color', 'value': ts.form_button_border_color, 'elements': ['el_form_button']},
                        {'label': 'Толщина линии обводки кнопки', 'type': 'borderWidth', 'name': 'form_button_border_width', 'value': ts.form_button_border_width, 'elements': ['el_form_button']},
                        {'label': 'Радиус скругления обводки кнопки', 'type': 'borderRadius', 'name': 'form_button_border_radius', 'value': ts.form_button_border_radius, 'elements': ['el_form_button']},
                    ],
                },
                {
                    'name': 'Стиль кнопок по умолчанию (В примере кнопка "НАЗАД")',
                    'inputs': [
                        {'label': 'Цвет кнопки', 'type': 'backgroundColor', 'name': 'form_button_back_default_color', 'value': ts.form_button_back_default_color, 'elements': ['el_form_button_start']},
                        {'label': 'Цвет текста кнопки', 'type': 'color', 'name': 'form_button_text_default_color', 'value': ts.form_button_text_default_color, 'elements': ['el_form_button_text_start']},
                        {'label': 'Цвет обводки кнопки', 'type': 'borderColor', 'name': 'form_button_border_default_color', 'value': ts.form_button_border_default_color, 'elements': ['el_form_button_start']},
                        {'label': 'Толщина линии обводки кнопки', 'type': 'borderWidth', 'name': 'form_button_border_default_width', 'value': ts.form_button_border_default_width, 'elements': ['el_form_button_start']},
                        {'label': 'Радиус скругления обводки кнопки', 'type': 'borderRadius', 'name': 'form_button_border_default_radius', 'value': ts.form_button_border_default_radius, 'elements': ['el_form_button_start']},
                    ],
                },
                {
                    'name': 'Линия над кнопками подвала',
                    'inputs': [
                        {'label': 'Цвет линии', 'type': 'backgroundColor', 'name': 'footer_line_color', 'value': ts.footer_line_color, 'elements': ['el_footer_line']  },
                        {'label': 'Толщина линии (px)', 'type': 'lineHeight', 'name': 'footer_line_height', 'value': ts.footer_line_height, 'elements': ['el_footer_line']  },
                    ]
                },
                {
                    'name': 'Линия левого меню',
                    'inputs': [
                        {'label': 'Цвет линии', 'type': 'backgroundColor', 'name': 'course_line_color', 'value': ts.course_line_color, 'elements': ['el_course_line']  },
                        {'label': 'Толщина линии (px)', 'type': 'lineHeight', 'name': 'course_line_height', 'value': ts.course_line_height, 'elements': ['el_course_line']  },
                    ]
                },
            ]
        }

        return render(request, 'customizer/customizer.html', context)

    def post(self, request):
        ts = ThemeSettings.objects.get(user=request.user)


        # Обновляем значения других полей из POST данных
        print(request.POST.items())
        for key, value in request.POST.items():
            if value == '.' or value == '':
                continue
            if key == 'is_back_course_page_enabled':
                print(value)
                value = value == 'on'
                print(value)

            if hasattr(ts, key):
                setattr(ts, key, value)

        ts.save()
        return redirect('custom_lesson')

class CardCustomizerView(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('signin') 
        return super().dispatch(request, *args, **kwargs)


    def get(self, request):
        emulator_size = {'width': 225, 'height': 275 }
        ts = ThemeSettings.objects.get(user=request.user)

        el_card_body = shape_factory(225, 275, ts.card_back_color, 0, 0, "el_card_body", border_radius=ts.card_border_radius, border_width=ts.card_border_width, border_color=ts.card_border_color)
        el_material_card_image = shape_factory(192, 75, "#7ee4d7", 16, 16, "el_material_card_image", border_radius=ts.card_image_border_radius, border_width=ts.card_image_border_width, border_color=ts.card_image_border_color)
        el_card_button = shape_factory(192.5, 32.5, ts.card_button_color,16, 225, "el_card_button", border_radius=ts.card_button_border_radius, border_width=ts.card_button_border_width, border_color=ts.card_button_border_color)

        el_card_bage = shape_factory(40, 15, ts.card_bage_background_color,20, 20, "el_card_bage", border_radius=0.9)
        el_card_bage_title = text_factory(28, 23, "el_card_bage_title", "Папка", 8, ts.card_bage_text_color)


        el_card_progress_bar_back = shape_factory(162.5, 6, ts.card_back_color, 16, 212, "el_card_progress_bar_back", ts.progress_card_border_radius, 1, ts.progress_card_border_color)  #настройка [+]
        el_card_progress = shape_factory(109, 4.3, ts.progress_card_bar_color, 16.8, 212.5, "el_card_progress", border_radius=0.1)
        el_card_progress_text = text_factory(190, 212, "el_card_secondary_text", "70%", 9, ts.card_text_color_secondary, 9)
        el_card_secondary_text = text_factory(16, 190, "el_card_secondary_text", "Описание курса", 9, ts.card_text_color_secondary, 9)
        el_card_title = text_factory(16, 105, "el_card_title", "Название курса", 13, ts.card_text_color_primary,13)
        el_button_title = text_factory(68, 235, "el_button_title", "ПРОДОЛЖИТЬ", 11, ts.card_button_color_primary,11)


        if ts.background_option == "background_image":
            device_browser_style = f''' style="background: url(/media/{ts.background_image}) no-repeat center center !important; background-size: cover !important;" '''
        else:
            device_browser_style = f'style="background-color: {ts.main_color}"'

        # Контекст для передачи в шаблон
        context = {
            'title': 'Настройка карточки курса',
            'device_browser_header' : False,
            'device_browser_style': device_browser_style,
            'base_layer': [el_card_body],
            'content_layer': [el_material_card_image, el_card_button, el_card_progress_bar_back],
            'overlay_layer': [el_card_progress, el_card_progress_text, el_card_secondary_text, el_card_title],
            'top_layer': [el_button_title, el_card_bage, el_card_bage_title],
            'emulator_size': emulator_size,
            'blocks': [
                {
                    'name': 'Карточка',
                    'inputs': [
                        {'label': 'Фон', 'type': 'backgroundColor', 'name': 'card_back_color', 'value': ts.card_back_color, 'elements': ['el_card_body']},
                        {'label': 'Цвет обводки', 'type': 'borderColor', 'name': 'card_border_color', 'value': ts.card_border_color, 'elements': ['el_card_body']},
                        {'label': 'Толщина линии обводки', 'type': 'borderWidth', 'name': 'card_border_width', 'value': ts.card_border_width, 'elements': ['el_card_body']},
                        {'label': 'Радиус скругления обводки', 'type': 'borderRadius', 'name': 'card_border_radius', 'value': ts.card_border_radius, 'elements': ['el_card_body']},
                    ],
                },
                {
                    'name': 'Бейдж',
                    'inputs': [
                        {'label': 'Фон', 'type': 'backgroundColor', 'name': 'card_bage_background_color', 'value': ts.card_bage_background_color, 'elements': ['el_card_bage']},
                        {'label': 'Цвет текста', 'type': 'color', 'name': 'card_bage_color', 'value': ts.card_bage_text_color, 'elements': ['el_card_bage_title']},
                    ],
                },
                {
                    'name': 'Изображение карточки',
                    'inputs': [
                        {'label': 'Цвет обводки', 'type': 'borderColor', 'name': 'card_image_border_color', 'value': ts.card_image_border_color, 'elements': ['el_material_card_image']},
                        {'label': 'Толщина линии обводки', 'type': 'borderWidth', 'name': 'card_image_border_width', 'value': ts.card_image_border_width, 'elements': ['el_material_card_image']},
                        {'label': 'Радиус скругления обводки', 'type': 'borderRadius', 'name': 'card_image_border_radius', 'value': ts.card_image_border_radius, 'elements': ['el_material_card_image']},
                    ],
                },
                {
                    'name': 'Текст карточки',
                    'inputs': [
                        {'label': 'Цвет заголовка', 'type': 'color', 'name': 'card_text_color_primary', 'value': ts.card_text_color_primary, 'elements': ['el_card_title']},
                        {'label': 'Цвет текста', 'type': 'color', 'name': 'card_text_color_secondary', 'value': ts.card_text_color_secondary, 'elements': ['el_card_secondary_text']},
                    ],
                },
                {
                    'name': 'Кнопка карточки',
                    'inputs': [
                        {'label': 'Цвет кнопки', 'type': 'backgroundColor', 'name': 'card_button_color', 'value': ts.card_button_color, 'elements': ['el_card_button']},
                        {'label': 'Цвет текста кнопки', 'type': 'color', 'name': 'card_button_color_primary', 'value': ts.card_button_color_primary, 'elements': ['el_button_title']},
                        {'label': 'Цвет обводки кнопки', 'type': 'borderColor', 'name': 'card_button_border_color', 'value': ts.card_button_border_color, 'elements': ['el_card_button']},
                        {'label': 'Толщина линии обводки кнопки', 'type': 'borderWidth', 'name': 'card_button_border_width', 'value': ts.card_button_border_width, 'elements': ['el_card_button']},
                        {'label': 'Радиус скругления обводки кнопки', 'type': 'borderRadius', 'name': 'card_button_border_radius', 'value': ts.card_button_border_radius, 'elements': ['el_card_button']},
                    ],
                },
                {
                    'name': 'Прогресс-бар',
                    'inputs': [
                        {'label': 'Цвет прогресс-бара', 'type': 'backgroundColor', 'name': 'progress_card_bar_color', 'value': ts.progress_card_bar_color, 'elements': ['el_card_progress']},
                        {'label': 'Цвет обводки прогресс-бара', 'type': 'borderColor', 'name': 'progress_card_border_color', 'value': ts.progress_card_border_color, 'elements': ['el_card_progress_bar_back']},
                        {'label': 'Толщина линии обводки прогресс-бара', 'type': 'borderWidth', 'name': 'progress_card_border_width', 'value': ts.progress_card_border_width, 'elements': ['el_card_progress_bar_back']},
                        {'label': 'Радиус скругления обводки прогресс-бара', 'type': 'borderRadius', 'name': 'progress_card_border_radius', 'value': ts.progress_card_border_radius, 'elements': ['el_card_progress_bar_back']},
                    ],
                },
            ]
        }
        return render(request, 'customizer/customizer.html', context)


    def post(self, request):
        ts = ThemeSettings.objects.get(user=request.user)
        
        for key, value in request.POST.items():
            if value == '.' or value == '':
                continue
            if hasattr(ts, key):
                setattr(ts, key, value)


        ts.save()
        return redirect('custom_card')

class LoginCustomizerView(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('signin') 
        return super().dispatch(request, *args, **kwargs)


    def get(self, request):
        emulator_size = {'width': 700, 'height': 400 }
        ts = ThemeSettings.objects.get(user=request.user)

        if ts.login_background_option == "login_background_image":
            background_image = ts.login_background_image
        else:
            background_image = ""

        el_login_card_body = shape_factory(220, 320, ts.login_card_back_color, 240, 40, "el_login_card_body", border_radius=ts.login_card_border_radius, border_width=ts.login_card_border_width, border_color=ts.login_card_border_color)
        el_login_background = shape_factory(emulator_size['width'], emulator_size['height'], ts.login_background_color, 0, 0, "el_login_background", background_image=background_image)

            
        el_logo = shape_factory(50, 50, "#858585", 325, 64, "el_logo", border_radius=0.1, border_width=0)
        el_login_school_name = text_factory(314, 133, "el_login_school_name", "School.name", 11, ts.login_school_color,12,"bold")
        el_title = text_factory(311, 154, "el_login_title", "Авторизация", 12, ts.login_title_color,12)

        el_email_label = text_factory(255, 186, "el_label", "* Email", 7, ts.login_label_color,7)
        el_input_email = shape_factory(190, 16, ts.login_input_back_color , 255, 200, "el_input", border_radius=ts.login_input_border_radius, border_width=ts.login_input_border_width, border_color=ts.login_input_border_color)
        el_text_field = text_factory(260, 241, "el_text_input", "*******", 9, ts.login_input_text_color ,9)

        el_password_label = text_factory(255, 224, "el_label", "* Пароль", 7, ts.login_label_color,7)     
        el_input_password = shape_factory(190, 16, ts.login_input_back_color , 255, 235, "el_input", border_radius=ts.login_input_border_radius, border_width=ts.login_input_border_width, border_color=ts.login_input_border_color)

        el_registration = text_factory(370, 284, "el_link", "Регистрация", 7, ts.login_link_label_color,7)     
        el_reset = text_factory(387, 224, "el_link", "Забыли пароль?", 7, ts.login_link_label_color,7)

        el_button = shape_factory(190, 16, ts.login_button_back_color , 255, 261, "el_button", border_radius=ts.login_button_border_radius, border_width=ts.login_button_border_width, border_color=ts.login_button_border_color)
        el_button_text = text_factory(338, 265, "el_button_text", "Войти", 8, ts.login_button_text_color,8)
        el_text_footer = text_factory(299, 284, "el_label", "У вас нет аккаунта?", 7, ts.login_label_color,7)


        sorted_options = [opt for opt in LOGIN_BACKGROUND_OPTIONS if opt[0] == ts.login_background_option]
        sorted_options += [opt for opt in LOGIN_BACKGROUND_OPTIONS if opt[0] != ts.login_background_option]

        # Контекст для передачи в шаблон
        context = {
            'title': 'Настройка карточки курса',
            'device_browser_header' : True,
            'device_browser_style': False,
            'base_layer': [el_login_background],
            'content_layer': [el_login_card_body],
            'overlay_layer': [el_logo, el_login_school_name, el_input_email, el_input_password, el_title, el_button],
            'top_layer': [el_email_label, el_password_label, el_reset, el_registration, el_text_footer, el_button_text, el_text_field],
            'emulator_size': emulator_size, 
            'blocks': [
                {
                    'name': 'Фон',
                    'inputs': [
                        {'label': 'Вариант оформления фона', 'type': 'select', 'name': 'login_background_option', 'options': sorted_options, 'elements': ['select']  },
                        {'label': 'Цвет фона', 'type': 'backgroundColor', 'name': 'login_background_color', 'value': ts.login_background_color, 'elements': ['el_login_background']},
                        {'label': 'Фоновое изображение', 'type': 'img', 'name': 'login_background_image', 'value': ts.login_background_image, 'elements': ['el_login_background']  },
                    ],
                },
                {
                    'name': 'Карточка',
                    'inputs': [
                        {'label': 'Фон', 'type': 'backgroundColor', 'name': 'login_card_back_color', 'value': ts.login_card_back_color, 'elements': ['el_login_card_body']},
                        {'label': 'Цвет обводки', 'type': 'borderColor', 'name': 'login_card_border_color', 'value': ts.login_card_border_color, 'elements': ['el_login_card_body']},
                        {'label': 'Толщина линии обводки', 'type': 'borderWidth', 'name': 'login_card_border_width', 'value': ts.login_card_border_width, 'elements': ['el_login_card_body']},
                        {'label': 'Радиус скругления обводки', 'type': 'borderRadius', 'name': 'login_card_border_radius', 'value': ts.login_card_border_radius, 'elements': ['el_login_card_body']},
                    ],
                },
                {
                    'name': 'Текст карточки',
                    'inputs': [
                        {'label': 'Цвет названия школы', 'type': 'color', 'name': 'login_school_color', 'value': ts.login_school_color, 'elements': ['el_login_school_name']},
                        {'label': 'Цвет залоговка', 'type': 'color', 'name': 'login_title_color', 'value': ts.login_title_color, 'elements': ['el_login_title']},
                        {'label': 'Цвет текста', 'type': 'color', 'name': 'login_label_color', 'value': ts.login_label_color, 'elements': ['el_label']},
                        {'label': 'Цвет ссылок', 'type': 'color', 'name': 'login_link_label_color', 'value': ts.login_link_label_color, 'elements': ['el_link']},
                    ],
                },
                {
                    'name': 'Поле ввода',
                    'inputs': [
                        {'label': 'Фон поля ввода', 'type': 'backgroundColor', 'name': 'login_input_back_color', 'value': ts.login_input_back_color, 'elements': ['el_input']},
                        {'label': 'Цвет текста поля ввода', 'type': 'color', 'name': 'login_input_text_color', 'value': ts.login_input_text_color, 'elements': ['el_text_input']},
                        {'label': 'Цвет обводки', 'type': 'borderColor', 'name': 'login_input_border_color', 'value': ts.login_input_border_color, 'elements': ['el_input']},
                        {'label': 'Толщина линии обводки', 'type': 'borderWidth', 'name': 'login_input_border_width', 'value': ts.login_input_border_width, 'elements': ['el_input']},
                        {'label': 'Радиус скругления обводки', 'type': 'borderRadius', 'name': 'login_input_border_radius', 'value': ts.login_input_border_radius, 'elements': ['el_input']},
                    ],
                },
                {
                    'name': 'Кнопка карточки',
                    'inputs': [
                        {'label': 'Цвет кнопки', 'type': 'backgroundColor', 'name': 'login_button_back_color', 'value': ts.login_button_back_color, 'elements': ['el_button']},
                        {'label': 'Цвет текста кнопки', 'type': 'color', 'name': 'login_button_text_color', 'value': ts.login_button_text_color, 'elements': ['el_button_text']},
                        {'label': 'Цвет обводки кнопки', 'type': 'borderColor', 'name': 'login_button_border_color', 'value': ts.login_button_border_color, 'elements': ['el_button']},
                        {'label': 'Толщина линии обводки кнопки', 'type': 'borderWidth', 'name': 'login_button_border_width', 'value': ts.login_button_border_width, 'elements': ['el_button']},
                        {'label': 'Радиус скругления обводки кнопки', 'type': 'borderRadius', 'name': 'login_button_border_radius', 'value': ts.login_button_border_radius, 'elements': ['el_button']},
                    ],
                },
            ]
        }
        return render(request, 'customizer/customizer.html', context)

    def post(self, request):
        ts = ThemeSettings.objects.get(user=request.user)
        
        for key, value in request.POST.items():
            if value == '.' or value == '':
                continue
            if hasattr(ts, key) and key != 'login_background_image':
                setattr(ts, key, value)


        if 'login_background_image' in request.FILES and request.FILES['login_background_image'].size > 0:
            ts.login_background_image = request.FILES['login_background_image']
        else:
            pass

        reset = request.POST.get('reset', 'false')
        if reset == 'true':
            default_image_path = 'backgrounds/default_background.png'
            ts.login_background_image = default_image_path

        ts.save()
        return redirect('custom_login')

class NavigationCustomizerView(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('signin') 
        return super().dispatch(request, *args, **kwargs)


    def get(self, request):
        emulator_size = {'width': 530, 'height': 240 }
        ts = ThemeSettings.objects.get(user=request.user)

        el_main_background = shape_factory(emulator_size['width'], emulator_size['height'], ts.main_color, 0, 0, "None")

        el_hr = shape_factory(510, 1, "#f0f0f0", 10, 37, "None")
        el_hr_active = shape_factory(240, 1, ts.hr_active_color, 266, 37, "el_hr_active")

        el_icon = custom_element_factory(115, 9, "el_icon", '<div style="width: 12px; height: 12px; background-color: #f0f0f0; border-radius: 50%; border: 0px solid transparent; display: flex; align-items: center; justify-content: center;" class="el_icon"><i class="bi bi-check" style="padding-top: 2px; color: #ffffff"></i></div>') #icon-dis 
        el_title_first_step = text_factory(136, 8, "None", "Теория", 10, ts.text_color ,10)
        el_sub_title_first_step = text_factory(134, 21, "None", "Завершено", 7, ts.text_color ,7)


        el_icon2 = custom_element_factory(408-37, 9, "el_icon_active", f'<div style="width: 12px; height: 12px; background-color: {ts.hr_active_color}; border-radius: 50%; border: 0px solid transparent; display: flex; align-items: center; justify-content: center;" class="el_icon_active"><i class="bi bi-check" style="padding-top: 2px; color: #ffffff"></i></div>')
        el_title_first_step2 = text_factory(425-37, 8, "None", "Оценка", 10, ts.text_color ,10)
        el_sub_title_first_step2 = text_factory(431-37, 21, "None", "10/10", 7, ts.text_color ,7)

        text1 = text_factory(18, 48, "None", "Оцените пройденный шаг", 12, ts.text_color )
        text2 = text_factory(18, 68, "None", "Ваша оценка помогает нам улучшить продукт", 8, ts.text_color)
        text3 = text_factory(18, 87, "None", "Выберите оценку", 7, ts.text_color)
        text5 = text_factory(18, 220, "None", "Пример цвета вашей", 7, ts.text_color)
        link = text_factory(93, 220, "el_link", "ссылки", 7, ts.link_color)


        base_left = 18
        offset = 25

        text_base_left = 25
        text_offset = 25

        el_shape1 = shape_factory(20, 20, ts.nps_back_color, base_left, 102, "el_shape", border_radius=ts.nps_border_radius, border_width=ts.nps_border_width, border_color=ts.nps_border_color)
        el_shape2 = shape_factory(20, 20, ts.nps_back_color, base_left + offset, 102, "el_shape", border_radius=ts.nps_border_radius, border_width=ts.nps_border_width, border_color=ts.nps_border_color)
        el_shape3 = shape_factory(20, 20, ts.nps_back_color, base_left + 2 * offset, 102, "el_shape", border_radius=ts.nps_border_radius, border_width=ts.nps_border_width, border_color=ts.nps_border_color)
        el_shape4 = shape_factory(20, 20, ts.nps_back_color, base_left + 3 * offset, 102, "el_shape", border_radius=ts.nps_border_radius, border_width=ts.nps_border_width, border_color=ts.nps_border_color)
        el_shape5 = shape_factory(20, 20, ts.nps_back_color, base_left + 4 * offset, 102, "el_shape", border_radius=ts.nps_border_radius, border_width=ts.nps_border_width, border_color=ts.nps_border_color)
        el_shape6 = shape_factory(20, 20, ts.nps_back_color, base_left + 5 * offset, 102, "el_shape", border_radius=ts.nps_border_radius, border_width=ts.nps_border_width, border_color=ts.nps_border_color)
        el_shape7 = shape_factory(20, 20, ts.nps_back_color, base_left + 6 * offset, 102, "el_shape", border_radius=ts.nps_border_radius, border_width=ts.nps_border_width, border_color=ts.nps_border_color)
        el_shape8 = shape_factory(20, 20, ts.nps_back_color, base_left + 7 * offset, 102, "el_shape", border_radius=ts.nps_border_radius, border_width=ts.nps_border_width, border_color=ts.nps_border_color)
        el_shape9 = shape_factory(20, 20, ts.nps_back_color, base_left + 8 * offset, 102, "el_shape", border_radius=ts.nps_border_radius, border_width=ts.nps_border_width, border_color=ts.nps_border_color)
        el_shape10 = shape_factory(20, 20, ts.nps_back_color, base_left + 9 * offset, 102, "el_shape", border_radius=ts.nps_border_radius, border_width=ts.nps_border_width, border_color=ts.nps_border_color)

        el_num_shape_1 = text_factory(text_base_left, 107, "el_num_shape", "1", 8, ts.nps_text_color)
        el_num_shape_2 = text_factory(text_base_left + text_offset, 107, "el_num_shape", "2", 8, ts.nps_text_color)
        el_num_shape_3 = text_factory(text_base_left + 2*text_offset, 107, "el_num_shape", "3", 8, ts.nps_text_color)
        el_num_shape_4 = text_factory(text_base_left + 3*text_offset, 107, "el_num_shape", "4", 8, ts.nps_text_color)
        el_num_shape_5 = text_factory(text_base_left + 4*text_offset, 107, "el_num_shape", "5", 8, ts.nps_text_color)
        el_num_shape_6 = text_factory(text_base_left + 5*text_offset + 1 , 107, "el_num_shape", "6", 8, ts.nps_text_color)
        el_num_shape_7 = text_factory(text_base_left + 6*text_offset + 0.5, 107, "el_num_shape", "7", 8, ts.nps_text_color)
        el_num_shape_8 = text_factory(text_base_left + 7*text_offset + 0.5, 107, "el_num_shape", "8", 8, ts.nps_text_color)
        el_num_shape_9 = text_factory(text_base_left + 8*text_offset, 107, "el_num_shape", "9", 8, ts.nps_text_color)
        el_num_shape_10 = text_factory(text_base_left + 9*text_offset -1, 107, "el_num_shape_end", "10", 8, "#ffffff")
       

        num_shapes = [el_num_shape_1, el_num_shape_2, el_num_shape_3, el_num_shape_4, el_num_shape_5, el_num_shape_6, el_num_shape_7, el_num_shape_8, el_num_shape_9, el_num_shape_10]
        shapes = [el_shape1, el_shape2, el_shape3, el_shape4, el_shape5, el_shape6, el_shape7, el_shape8, el_shape9, el_shape10]

        text4 = text_factory(18, 135, "None", "Поясните почему вы поставили такую оценку", 7, ts.text_color, 7, "bold")

        el_form = shape_factory(477, 26, ts.main_color , 18, 149, "el_form", border_radius=ts.form_border_radius, border_width=ts.form_border_width, border_color=ts.form_border_color)

        el_form_button = shape_factory(60, 15, ts.form_button_back_color , 18, 180, "el_form_button", border_radius=ts.form_button_border_radius, border_width=ts.form_button_border_width, border_color=ts.form_button_border_color)

        el_form_button_text = text_factory(27, 184, "None", 'Отправить <i class="bi bi-send"></i>', 6, ts.form_button_text_color, 6)

        el_form_text = text_factory(25, 155, "el_form_text", 'Потому, что ...', 6, ts.form_button_text_color, 6)

        # Контекст для передачи в шаблон
        context = {
            'title': 'Настройка кнопок, форм и элементов ввода',
            'device_browser_header' : True,
            'device_browser_style': False,
            'base_layer': [el_main_background],
            'content_layer': [el_hr, el_icon, el_title_first_step, el_sub_title_first_step, el_icon2, el_title_first_step2, el_sub_title_first_step2],
            'overlay_layer': [el_hr_active,text1, text2, text3, text4, el_form, el_form_button, text5, link]  + shapes,
            'top_layer': [el_form_button_text, el_form_text] + num_shapes,
            'emulator_size': emulator_size,
            'blocks': [
                {
                    'name': 'Активный этапа',
                    'inputs': [
                        {'label': 'Цвет активного этапа', 'type': 'backgroundColor', 'name': 'hr_active_color', 'value': ts.hr_active_color, 'elements': ['el_hr_active', 'el_icon_active']},
                    ],
                },
                {
                    'name': 'Кнопки оценки курса',
                    'inputs': [
                        {'label': 'Цвет кнопки', 'type': 'backgroundColor', 'name': 'nps_back_color', 'value': ts.nps_back_color, 'elements': ['el_shape']},
                        {'label': 'Цвет текста кнопки', 'type': 'color', 'name': 'nps_text_color', 'value': ts.nps_text_color, 'elements': ['el_shape', 'el_num_shape']},
                        {'label': 'Цвет обводки кнопки', 'type': 'borderColor', 'name': 'nps_border_color', 'value': ts.nps_border_color, 'elements': ['el_shape', 'el_num_shape_end']},
                        {'label': 'Толщина линии обводки кнопки', 'type': 'borderWidth', 'name': 'nps_border_width', 'value': ts.nps_border_width, 'elements': ['el_shape', 'el_num_shape_end']},
                        {'label': 'Радиус скругления обводки кнопки', 'type': 'borderRadius', 'name': 'nps_border_radius', 'value': ts.nps_border_radius, 'elements': ['el_shape', 'el_num_shape_end']},
                    ],
                },
                {
                    'name': 'Поле ввода',
                    'inputs': [
                        {'label': 'Фон поля ввода', 'type': 'backgroundColor', 'name': 'form_back_color', 'value': ts.form_back_color, 'elements': ['el_form']},
                        {'label': 'Цвет текста поля ввода', 'type': 'color', 'name': 'form_text_color', 'value': ts.form_text_color, 'elements': ['el_form_text']},
                        {'label': 'Цвет обводки', 'type': 'borderColor', 'name': 'form_border_color', 'value': ts.form_border_color, 'elements': ['el_form']},
                        {'label': 'Толщина линии обводки', 'type': 'borderWidth', 'name': 'form_border_width', 'value': ts.form_border_width, 'elements': ['el_form']},
                        {'label': 'Радиус скругления обводки', 'type': 'borderRadius', 'name': 'form_border_radius', 'value': ts.form_border_radius, 'elements': ['el_form']},
                    ]
                },
                {
                    'name': 'Цвет ссылки',
                    'inputs': [
                        {'label': 'Цвет ссылки', 'type': 'color', 'name': 'link_color', 'value': ts.link_color, 'elements': [ 'el_link']},
                    ],
                },
            ]
        }
        return render(request, 'customizer/customizer.html', context)


    def post(self, request):
        ts = ThemeSettings.objects.get(user=request.user)

        for key, value in request.POST.items():
            if value == '.' or value == '':
                continue
            if hasattr(ts, key):
                setattr(ts, key, value)
        ts.save()
        return redirect('custom_navigation')

class ScriptCustomizerView(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('signin') 
        return super().dispatch(request, *args, **kwargs)


    def get(self, request):
        ts = ThemeSettings.objects.get(user=request.user)
        context = {
            'uuid': request.user.uuid,
            'domain': request.user.domain,
            'body_html': request.user.body_html,
            'head_html': request.user.head_html,
            'ts': ts,
        }
        return render(request, 'customizer/script.html', context)


    def post(self, request):
        request.user.domain = request.POST.get('domain')
        if request.POST.get('body_html'):
            request.user.body_html = request.POST.get('body_html')
        if request.POST.get('head_html'):
            request.user.head_html = request.POST.get('head_html')
        request.user.save()
        return redirect('custom_script')
    



class BanerCustomizerView(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('signin') 
        return super().dispatch(request, *args, **kwargs)


    def get(self, request):
        ts = ThemeSettings.objects.get(user=request.user)

        if ts.baner_image == 'baners/default_baner.png':
            reset_baner = 'true'
        else:
            reset_baner = 'false'

        if ts.baner_mob_image == 'baners/default_baner.png':
            reset_baner_mob = 'true'
        else:
            reset_baner_mob = 'false'

        print(reset_baner)

        context = {
            'title': 'Настройка бокового банера',
            'emulator_hide': True,
            'reset_baner': reset_baner,
            'reset_baner_mob': reset_baner_mob,
            'blocks': [
                {
                    'name': 'Банер',
                    'inputs': [
                        {'label': 'Картинка  на декстоп ( рекомендуемая ширина 300px )', 'type': 'baner', 'name': 'baner_image', 'value': ts.baner_image, 'elements': []  },
                        {'label': 'Картинка  на мобильную версию ( рекомендуемая ширина 450px )', 'type': 'baner_mob', 'name': 'baner_mob_image', 'value': ts.baner_mob_image, 'elements': []  },
                        {'label': 'Cсылка на банера', 'type': 'url', 'name': 'banner_url', 'value': ts.banner_url, 'elements': []},
                    ],
                },
                {
                    'name': 'Ссылки на социальные сети (необязательно)',
                    'inputs': [
                        {'label': 'Ссылка на Телеграм', 'type': 'url', 'name': 'telegram_url', 'value': ts.telegram_url, 'elements': []},
                        {'label': 'Ссылка на Инстаграм', 'type': 'url', 'name': 'instagram_url', 'value': ts.instagram_url, 'elements': []},
                        {'label': 'Ссылка на ВКонтакте', 'type': 'url', 'name': 'vk_url', 'value': ts.vk_url, 'elements': []},
                        {'label': 'Ссылка на X (Twitter)', 'type': 'url', 'name': 'x_url', 'value': ts.x_url, 'elements': []},
                        {'label': 'Ссылка на YouTube', 'type': 'url', 'name': 'youtube_url', 'value': ts.youtube_url, 'elements': []},
                        {'label': 'Ссылка на WhatsApp', 'type': 'url', 'name': 'whatsapp_url', 'value': ts.whatsapp_url, 'elements': []},
                    ],
                },
            ]
        }
        return render(request, 'customizer/customizer.html', context)


    def post(self, request):
        ts = ThemeSettings.objects.get(user=request.user)
        
        print(request.POST.items())
        for key, value in request.POST.items():
            if value == '.' or value == '':
                if 'url' in key:
                    pass
                else:
                    continue

            if hasattr(ts, key):
                setattr(ts, key, value)

        
        if 'baner_image' in request.FILES and request.FILES['baner_image'].size > 0:
            ts.baner_image = request.FILES['baner_image']
        else:
            pass

        if 'baner_mob_image' in request.FILES and request.FILES['baner_mob_image'].size > 0:
            ts.baner_mob_image = request.FILES['baner_mob_image']
        else:
            pass

        reset_baner = request.POST.get('reset_baner', 'false')
        reset_baner_mob = request.POST.get('reset_baner_mob', 'false')
        print(reset_baner)
        if reset_baner == 'true':
            default_image_path = 'baners/default_baner.png'
            ts.baner_image = default_image_path

        if reset_baner_mob == 'true':
            default_image_path = 'baners/default_baner.png'
            ts.baner_mob_image = default_image_path

        ts.save()
        return redirect('baner')