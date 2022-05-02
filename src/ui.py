from gameplay.hammers import Hammers
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


def init():
    UI.debug_manager = gui.UIManager(GS.win_size, "data/debug_ui_theme.json")

    UI.ui_manager = gui.UIManager(GS.win_size, "data/ui_theme.json")
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

    UI.ui_manager.process_events(e)


def frame():
    UI.ui_manager.update(GS.dt)

    if UI.active_prompt is not None:
        UI.active_prompt.frame()
    if UI.prompt_in_hide is not None:
        UI.prompt_in_hide.frame()

    UI.ui_manager.draw_ui(GS.win_surface)
