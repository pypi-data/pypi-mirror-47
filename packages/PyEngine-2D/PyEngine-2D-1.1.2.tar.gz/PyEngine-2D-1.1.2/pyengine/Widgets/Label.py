from pyengine.Widgets.Widget import Widget
from pyengine.Utils import Font, Color, Colors

__all__ = ["Label"]


class Label(Widget):
    def __init__(self, position, text, color=Colors.WHITE.value, font=None):
        super(Label, self).__init__(position)
        if font is None:
            font = Font()

        if not isinstance(font, Font):
            raise TypeError("Font have not a Font type")
        if not isinstance(color, Color):
            raise TypeError("Color have not a Color type")

        self.color = color
        self.font = font
        self.text = text
        self.update_render()

    def set_color(self, color):
        if not isinstance(color, Color):
            raise TypeError("Color have not a Color type")

        self.color = color
        self.update_render()

    def get_color(self):
        return self.color

    def set_font(self, font):
        if not isinstance(font, Font):
            raise TypeError("Font have not a Font type")

        self.font = font
        self.update_render()

    def get_font(self):
        return self.font

    def get_text(self):
        return self.text

    def set_text(self, text):
        self.text = text
        self.update_render()

    def update_render(self):
        self.image = self.font.render().render(self.text, 1, self.color.get())
        self.update_rect()
        if self.parent:
            self.parent.update_render()

