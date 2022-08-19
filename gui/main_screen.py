from auto_components.button import Button
from auto_components.control_point import ControlPoint
from auto_components.horizontal_grid import HorizontalGrid
from auto_components.popup_window import PopupWindow
from auto_components.required_point import RequiredPoint
from auto_components.vertical_grid import VerticalGrid
from auto_components.way_point import WayPoint
from base.dimensions import Dimensions
from gui_components.component import Component
from gui_components.grid import Grid
from gui_components.screen import Screen
from base.colors import *
from base.important_variables import *
from base.velocity_calculator import VelocityCalculator
from pygame_abstraction.utility_functions import set_mouse_position
from auto_components.draggable_component import DraggableComponent

class MainScreen(Screen):
    # Miscellaneous
    draggable_components = []
    new_draggable_components = [] # Components that need to be added to draggable_components next cycle (has to do with a weird clicking glitch)
    control_points = []
    way_points = []
    required_points = []
    component_length = DraggableComponent.base_length * DraggableComponent.selected_size_multiplier
    font_size = 22
    toolbar_dimensions = None
    current_popup = None
    has_popup = False
    selected_component = None #TODO add selecting components

    # Toolbar Buttons
    draw_button = Button("Draw", font_size, pleasing_green, dark_green, white)
    save_button = Button("Save", font_size, pleasing_green, dark_green, white)
    show_way_points_button = Button("Show Way Points", font_size, way_point_color, selected_way_point_color, white)
    show_control_points_button = Button("Show Control Points", font_size, control_point_color, selected_control_point_color, white)
    show_required_points_button = Button("Show Required Points", font_size, required_point_color, selected_required_point_color, white)

    # Draggable Component Buttons
    way_point_button = Button("Create Way Point", font_size, way_point_color, selected_way_point_color, white)
    control_point_button = Button("Create Control Point", font_size, control_point_color, selected_control_point_color, white)
    required_point_button = Button("Create Required Point", font_size, required_point_color, selected_required_point_color, white)
    divider_line = Component("")  # Used to divide the space between the buttons and where the components 'spawn'

    # Toolbar Modifiable Numbers
    toolbar_length = VelocityCalculator.get_measurement(screen_length, 100)
    toolbar_height = VelocityCalculator.get_measurement(screen_height, 15)
    toolbar_vertical_buffer = VelocityCalculator.get_measurement(screen_height, 5)

    # Component Bar Modifiable Numbers
    component_bar_length = VelocityCalculator.get_measurement(screen_length, 23)
    divider_line_length = VelocityCalculator.get_measurement(screen_length, 1)

    # Items in the bars
    toolbar = [draw_button, save_button, show_way_points_button, show_control_points_button, show_required_points_button]
    component_bar = [way_point_button, control_point_button, required_point_button]

    def __init__(self):
        super().__init__("")

        toolbar_grid = HorizontalGrid(Dimensions(0, 0, self.toolbar_length, self.toolbar_height), 1, None)
        toolbar_grid.turn_into_grid(self.toolbar, screen_length / 2, None)

        self.toolbar_dimensions = toolbar_grid.dimensions

        self.create_component_bar()

    def create_component_bar(self):
        bar_top_edge = self.toolbar_height + self.toolbar_vertical_buffer
        bar_height = screen_height - bar_top_edge
        bar_left_edge = screen_length - self.component_bar_length

        component_bar_grid = HorizontalGrid(Dimensions(bar_left_edge, bar_top_edge, self.component_bar_length, bar_height), None, 1)
        component_bar_grid.turn_into_grid(self.component_bar, None, bar_height / 2)

        self.divider_line.number_set_dimensions(bar_left_edge - self.divider_line_length, bar_top_edge, self.divider_line_length, bar_height)
        self.divider_line.color = black
        self.component_bar.append(self.divider_line)

    def run(self):
        self.draggable_components += self.new_draggable_components
        self.new_draggable_components = []

        self.run_bar_clicking(self.component_bar, self.spawn_component)
        self.run_bar_clicking(self.toolbar, self.open_toolbar_popup)

        self.set_component_bounds()

        if self.current_popup is not None:
            self.run_popup()

    def run_popup(self):
        if self.current_popup.is_finished:
            self.current_popup.reset()
            self.has_popup = False

        self.current_popup.run()

    def open_toolbar_popup(self, button):
        button_to_popup = {self.save_button: PopupWindow([]),
                           self.show_control_points_button: PopupWindow([]),
                           self.show_required_points_button: PopupWindow([]),
                           self.show_way_points_button: PopupWindow([])}

        popup = button_to_popup.get(button)

        if button != self.draw_button:
            self.current_popup = popup
            self.has_popup = True

    def run_bar_clicking(self, bar_components, function):
        """Runs what should happen when a bar is clicked (like a toolbar)"""

        for button in bar_components:
            if button.got_clicked():
                function(button)

    def spawn_component(self, button):
        left_edge = self.divider_line.left_edge - self.component_length
        top_edge = button.vertical_midpoint

        button_to_component = {self.way_point_button: [WayPoint, self.way_points],
                               self.required_point_button: [RequiredPoint, self.required_points],
                               self.control_point_button: [ControlPoint, self.control_points]}

        component_class, component_list = button_to_component.get(button)
        component = component_class(left_edge, top_edge)
        component_list.append(component)

        self.new_draggable_components.append(component)

        set_mouse_position(component.horizontal_midpoint, component.vertical_midpoint)

    def set_component_bounds(self):
        for component in self.draggable_components:
            min_top_edge = self.toolbar_dimensions.bottom_edge
            max_top_edge = screen_height - component.height
            min_left_edge = 0
            max_left_edge = self.divider_line.left_edge - component.length

            component.set_bounds(min_top_edge, max_top_edge, min_left_edge, max_left_edge)

    def get_components(self):
        screen_components = self.toolbar + self.draggable_components + self.component_bar
        return self.current_popup.get_components() if self.has_popup else screen_components