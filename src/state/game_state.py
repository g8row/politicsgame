import pygame
import pygame
import pygame_gui as gui

#
# Глобални променливи, повечето от тях се сетват от main.py
#

win_size: tuple[int, int] = (800, 600)
win: pygame.surface.Surface

world_render_target: pygame.surface.Surface     # Самия свят (стаята) се рисува тук
center: tuple[int, int]     # Кординати на центъра на екрана, за центриране на неща

# Тук се слагат картинки, които се четат докато зарежда играта в началото,
# за да не се четат от файла всеки път като се рисуват
images: dict[str, pygame.surface.Surface] = {}

# Колко секунди имаме на frame (0.016 за 60 fps),
# използва се за сметки, които включват време (анимации, физика и т.н.)
dt: float
