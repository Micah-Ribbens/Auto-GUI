from math import floor

from gui_components.grid import Grid


class HorizontalGrid(Grid):
    def get_column_number(self, item_number, rows, columns):
        return item_number % columns

    def get_row_number(self, item_number, rows, columns):
        return floor(item_number / columns)