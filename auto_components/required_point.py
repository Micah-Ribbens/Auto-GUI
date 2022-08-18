from auto_components.draggable_component import DraggableComponent
from base.colors import *

class RequiredPoint(DraggableComponent):
    def __init__(self, left_edge, top_edge):
        super().__init__(left_edge, top_edge, required_point_color, selected_required_point_color, None)
