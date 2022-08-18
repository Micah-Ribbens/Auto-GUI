from auto_components.draggable_component import DraggableComponent
from base.colors import *

class ControlPoint(DraggableComponent):
    def __init__(self, left_edge, top_edge):
        super().__init__(left_edge, top_edge, control_point_color, selected_control_point_color, None)
