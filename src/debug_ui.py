from pygame.event import Event
from debug.debug_console import DebugConsole
import state.game_state as GS
import state.ui_state as UI

import pygame
import pygame_gui as gui

from typing import List


def init():
    UI.debug_console = DebugConsole()


def on_event(e: Event):
    # TODO: Да направим DebugConsole UIElement, така че да не
    # трябва да го третираме като "отделно нещо"
    UI.debug_console.on_event(e)
    UI.debug_manager.process_events(e)


def frame():
    UI.debug_manager.update(GS.dt)
    UI.debug_manager.draw_ui(GS.win_surface)
