from gui_components.text_box import TextBox
from pygame_abstraction.utility_functions import is_mouse_collision


class Button(TextBox):
    default_color = None
    hover_color = None

    def __init__(self, text, font_size, default_color, hover_color, text_color):
        super().__init__(text, font_size, default_color, text_color, True)
        self.default_color, self.hover_color = default_color, hover_color

    def run(self):
        color = self.hover_color if is_mouse_collision(self) else self.default_color
        self.set_color(color)