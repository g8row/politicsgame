from typing import Dict
import pygame
import pygame_gui as gui

#
# Глобални променливи, повечето от тях се сетват от main.py
#

win_size: tuple[int, int] = (800, 600)
win_surface: pygame.surface.Surface
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

from gameplay.calendar import Calendar
from gameplay.metrics import Metrics
from gameplay.hammers import Hammers

calendar: Calendar
metrics: Metrics
hammers: Hammers

economy: int = 50     # 0-100
approval: int = 55     # 0-100
oligarchs: int = 70     # 0-100


def add_economy(amount: int):
    global economy
    global to_show_protest_end
    
    economy += amount
    if economy < 0:
        economy = 0
        to_show_protest_end = True
    if economy > 100:
        economy = 100

    metrics.set_marker_percentage(0, economy / 100)


def add_approval(amount: int):
    global approval
    global to_show_protest_end

    approval += amount
    if approval < 0:
        approval = 0
        to_show_protest_end = True
    if approval > 100:
        approval = 100

    metrics.set_marker_percentage(1, approval / 100)


def add_oligarchs(amount: int):
    global oligarchs
    global to_show_bad_end

    oligarchs += amount
    if oligarchs < 0:
        oligarchs = 0
        to_show_bad_end = True
    if oligarchs > 100:
        oligarchs = 100


butter_inf_campaign: bool = False
decision_one: bool = False     #Отбелязваме кои прозорци след кои решения идват
decision_two: bool = False
econ_growth: int = 0     #Променлива, която означава с колко процента дневно се променя икономиката

to_show_good_end: bool = False
to_show_bad_end: bool = False
to_show_protest_end: bool = False
