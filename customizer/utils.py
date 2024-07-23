class BaseElement:
    def __init__(self, left, top, class_id):
        self.left = left
        self.top = top
        self.class_id = class_id

    def render(self, inner_html=""):
        return f'''
        <div class="position-absolute" style="left: {self.left}px; top: {self.top}px;">
            {inner_html}
        </div>
        '''

    def is_instance_of(self, class_name):
        return self.__class__.__name__ == class_name


class Shape(BaseElement):
    def __init__(self, width, height, background_color, left, top, class_id, border_radius=None, border_width=None, border_color=None, background_image=""):     
        super().__init__(left, top, class_id)
        self.width = width
        self.height = height
        self.background_color = background_color
        self.border_radius = border_radius or 0
        self.border_width = border_width or 0
        self.border_color = border_color or "transparent"
        self.background_image = str(background_image)

    def render(self):
        print(f'background-image: url("media/{self.background_image}");')
        shape_html = f'''
        <div class="{self.class_id}"
            id="{self.class_id}" 
            style="
            width: {self.width}px;
            height: {self.height}px;
            background-color: {self.background_color};
            border-radius: {self.border_radius}rem;
            border: {self.border_width}px solid {self.border_color};
            background-image: url('media/{self.background_image}');
            ">
        </div>
        '''
        return super().render(inner_html=shape_html)


class Circle(Shape):
    def __init__(self, diameter, background_color, left, top, class_id, border_width=None, border_color=None):
        super().__init__(
            width=diameter,
            height=diameter,
            background_color=background_color,
            left=left,
            top=top,
            class_id=class_id,
            border_radius=50,
            border_width=border_width, 
            border_color=border_color
        )

    def render(self):
        circle_html = f'''
        <div class="position-absolute" style="left: {self.left}px; top: {self.top}px;">
        <div style="
            width: {self.width}px;
            height: {self.height}px;
            background-color: {self.background_color};
            border-radius: {self.border_radius}rem;
            border: {self.border_width}px solid {self.border_color};" class="{self.class_id}">
        </div>
        </div>
        '''
        return circle_html


class Text(BaseElement):
    def __init__(self, left, top, class_id, text, font_size, color, line_height, font_weight="normal", font_style="normal"):
        super().__init__(left, top, class_id)
        self.text = text
        self.font_size = font_size 
        self.color = color
        self.font_weight = font_weight 
        self.font_style = font_style
        self.line_height = line_height 

    def render(self):
        text_html = f'''
        <p style="line-height: {self.line_height}px; font-size: {self.font_size}px; color: {self.color}; font-weight: {self.font_weight}; font-style: {self.font_style};" class="{self.class_id}">
            {self.text}
        </p>
        '''
        return super().render(inner_html=text_html)
        

class Image(BaseElement):
    def __init__(self, left, top, class_id, image_name,  border_radius=None, border_width=None, border_color=None):
        super().__init__(left, top, class_id)
        self.image_name = image_name
        self.border_radius = border_radius or 0
        self.border_width = border_width or 0
        self.border_color = border_color or "transparent"

    def render(self):
        image_html = f'''
        <img src="/static/elements/{self.image_name}" 
        style="position: absolute; 
            left: {self.left}px;
            top: {self.top}px; 
            border-radius: {self.border_radius}rem;
            border: {self.border_width}px solid {self.border_color};"
            class="{self.class_id}">
        '''
        return image_html

class CustomElement(BaseElement):
    def __init__(self, left, top, class_id, html_content):
        super().__init__(left, top, class_id)
        self.html_content = html_content

    def render(self):
        return super().render(inner_html=self.html_content)