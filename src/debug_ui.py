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
    UI.debug_console.on_event(e)


def frame():
    pass
