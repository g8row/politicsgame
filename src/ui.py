from gameplay.hammers import Hammers
from prompts.prompt_ending import PromptEnding
import state.game_state as GS
import state.ui_state as UI

from pygame.event import Event
import pygame
import pygame_gui as gui

from prompts.prompt_just_ok import PromptJustOk
from prompts.prompt_ask_for_identity import PromptAskForIdentity
from gameplay.calendar import Calendar
from gameplay.metrics import Metrics
from gameplay.hammers import Hammers

import os


def init():
    debug_ui_theme = os.path.join(os.getcwd(), "data", "debug_ui_theme.json")
    ui_theme = os.path.join(os.getcwd(), "data", "ui_theme.json")

    UI.debug_manager = gui.UIManager(GS.win_size, debug_ui_theme)

    UI.ui_manager = gui.UIManager(GS.win_size, ui_theme)
    UI.ui_manager.add_font_paths("Pala", regular_path="data/fonts/pala.ttf", bold_path="data/fonts/palab.ttf")
    UI.ui_manager.preload_fonts(
        [
            {
                "name": "Pala",
                "point_size": 14,
                "style": "regular"
            }, {
                "name": "Pala",
                "point_size": 14,
                "style": "bold"
            }, {
                'name': 'Pala',
                'point_size': 14,
                'style': 'italic'
            }, {
                "name": "Pala",
                "point_size": 16,
                "style": "regular"
            }, {
                "name": "Pala",
                "point_size": 18,
                "style": "regular"
            }
        ]
    )

    GS.calendar = Calendar()
    GS.metrics = Metrics()
    GS.hammers = Hammers()


def on_event(e: Event):
    if UI.active_prompt is not None:
        UI.active_prompt.on_event(e)

    if e.type == pygame.KEYDOWN and e.key == pygame.K_F3:
        UI.prompt(PromptJustOk(title="Здравей", desc_html="Баница"))

    if e.type == pygame.KEYDOWN and e.key == pygame.K_F4:
        GS.to_show_good_end = True

    if e.type == pygame.KEYDOWN and e.key == pygame.K_F5:
        GS.to_show_protest_end = True

    if e.type == pygame.KEYDOWN and e.key == pygame.K_F6:
        GS.to_show_bad_end = True

    UI.ui_manager.process_events(e)

def frame():
    UI.ui_manager.update(GS.dt)

    if UI.active_prompt is not None:
        UI.active_prompt.frame()
    if UI.prompt_in_hide is not None:
        UI.prompt_in_hide.frame()

    UI.ui_manager.draw_ui(GS.win_surface)
