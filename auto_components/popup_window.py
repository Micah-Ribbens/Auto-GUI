from gui_components.component import Component
from gui_components.screen import Screen
from base.velocity_calculator import VelocityCalculator
from base.important_variables import *
from base.utility_functions import *


class PopupWindow(Screen):
    back_arrow_default_image_path = "images/default_back_arrow.png"
    back_arrow_hover_image_path = "images/hover_back_arrow.png"
    back_arrow = Component("images/default_back_arrow.png")
    back_arrow_image_paths = [back_arrow_default_image_path, back_arrow_hover_image_path]
    back_arrow_length = VelocityCalculator.get_measurement(screen_length, 6)
    back_arrow_height = VelocityCalculator.get_measurement(screen_height, 4)

    is_finished = False

    def __init__(self, components):
        self.back_arrow.number_set_dimensions(20, 20, self.back_arrow_length, self.back_arrow_height)
        self.components = components + [self.back_arrow]

        for image_path in self.back_arrow_image_paths:
            load_image(image_path)

    def run(self):
        super().run()

        if self.back_arrow.got_clicked():
            self.is_finished = True

        mouse_is_on_back_arrow = is_mouse_collision(self.back_arrow)
        self.back_arrow.path_to_image = self.back_arrow_hover_image_path if mouse_is_on_back_arrow else self.back_arrow_default_image_path

    def reset(self):
        self.is_finished = False

    def get_is_finished(self):
        return self.is_finished


