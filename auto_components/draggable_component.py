from auto_components.popup_window import PopupWindow
from base.important_variables import *
from base.utility_functions import mouse_is_clicked
from gui_components.component import Component
from pygame_abstraction.utility_functions import get_mouse_position
from base.velocity_calculator import VelocityCalculator
from base.important_variables import *


class DraggableComponent(Component):
    # Miscellaneous
    is_selected = True
    pop_up_window = None
    color = None
    base_color = None
    selected_color = None
    base_size_multiplier = 1
    selected_size_multiplier = 1.3
    bounds = []

    # Size
    base_length = VelocityCalculator.get_measurement(screen_length, 4)
    base_height = base_length

    def __init__(self, left_edge, top_edge, base_color, selected_color, pop_up_window):
        # TODO Change this
        if self.pop_up_window is None:
            self.pop_up_window = PopupWindow([])

        super().__init__("")

        self.color, self.base_color = base_color, base_color
        self.pop_up_window, self.selected_color = pop_up_window, selected_color

        self.number_set_dimensions(left_edge, top_edge, self.base_length, self.base_height)
        self.bounds = [0, screen_height, 0, screen_length]

    def run(self):
        if self.is_selected and mouse_is_clicked():
            self.is_selected = False

        if self.is_selected:
            self.run_selection_movement()

        size_multiplier = self.selected_size_multiplier if self.is_selected else self.base_size_multiplier

        self.length = self.base_length * size_multiplier
        self.height = self.base_height * size_multiplier

    def run_selection_movement(self):
        mouse_left_edge, mouse_top_edge = get_mouse_position()

        self.left_edge = mouse_left_edge - self.length / 2
        self.top_edge = mouse_top_edge - self.height / 2

        min_top_edge, max_top_edge, min_left_edge, max_left_edge = self.bounds

        self.left_edge = min_left_edge if self.left_edge < min_left_edge else self.left_edge
        self.left_edge = max_left_edge if self.left_edge > max_left_edge else self.left_edge

        self.top_edge = min_top_edge if self.top_edge < min_top_edge else self.top_edge
        self.top_edge = max_top_edge if self.top_edge > max_top_edge else self.top_edge

    def set_bounds(self, min_top_edge, max_top_edge, min_left_edge, max_left_edge):
        self.bounds = [min_top_edge, max_top_edge, min_left_edge, max_left_edge]

    def render(self):
        self.color = self.selected_color if self.is_selected else self.base_color
        super().render()