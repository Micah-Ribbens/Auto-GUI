import cProfile

from base.game_runner_function import *
from gui.main_screen import MainScreen

cProfile.run("run_game(MainScreen())", None, "tottime")