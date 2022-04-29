from typing import Dict
import pygame
import pygame
import pygame_gui as gui

#
# Глобални променливи, повечето от тях се сетват от main.py
#

win_size: tuple[int, int] = (800, 600)
win_surface: pygame.surface.Surface
non_animated_ui_surface: pygame.surface.Surface

world_render_target: pygame.surface.Surface     # Самия свят (стаята) се рисува тук
center: tuple[int, int]     # Кординати на центъра на екрана, за центриране на неща

# Тук се слагат картинки, които се четат докато зарежда играта в началото,
# за да не се четат от файла всеки път като се рисуват
images: dict[str, pygame.surface.Surface] = {}

# Колко секунди имаме на frame (0.016 за 60 fps),
# използва се за сметки, които включват време (анимации, физика и т.н.)
dt: float

time_in_game = 0     # Измерва се в четвърт-дни, за да вземеш деня раздели на 4
current_day = -1     # time_in_game / 4, закръглено

time_speed_default = 2     # Мери се в четвърт-дни за секунда
time_speed = time_speed_default     # Слага се на 0 (паузира), когато има меню отворено

# Чете се от script.py, първо е деня, после str с constructor-а
# на prompt-а като валиден Python код.
script: dict[int, list[str]] = {}

# Първо се чете тук, ако има грешка се прекъсва и не се записва в script
script_parsed: dict[int, list[str]] = {}
