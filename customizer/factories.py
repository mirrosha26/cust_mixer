from .utils import Shape, Circle, Text, Image,CustomElement

# Фабрики для создания элементов
def shape_factory(width, height, background_color, left, top, class_id, border_radius=0, border_width=0, border_color="transparent"):
    return Shape(
        width=width,
        height=height,
        background_color=background_color,
        left=left,
        top=top,
        class_id=class_id,
        border_radius=border_radius,
        border_width=border_width,
        border_color=border_color
    )

def circle_factory(diameter, background_color, left, top, class_id, border_width=0, border_color="transparent"):
    return Circle(
        diameter=diameter,
        background_color=background_color,
        left=left,
        top=top,
        class_id=class_id,
        border_width=border_width,
        border_color=border_color
    )

def text_factory(left, top, class_id, text, font_size, color, line_height=None, font_weight="normal", font_style="normal"):
    if not line_height:
        line_height = font_size
    return Text(
        left=left,
        top=top,
        class_id=class_id,
        text=text,
        font_size=font_size,
        color=color,
        line_height=line_height,
        font_weight=font_weight,
        font_style=font_style
    )

def image_factory(left, top, class_id, image_name,  border_radius=None, border_width=None, border_color=None):
    return Image(
        left=left,
        top=top,
        class_id=class_id,
        image_name=image_name,
        border_radius=border_radius,
        border_width=border_width,
        border_color=border_color
    )


def custom_element_factory(left, top, class_id, html_content):
    return CustomElement(
        left=left,
        top=top,
        class_id=class_id,
        html_content=html_content
    )