from pygame.event import Event
from state import GameState
import pygame
import pygame_gui

from typing import Tuple


def init(gs: GameState):
    gs.console = pygame_gui.windows.UIConsoleWindow(
        rect=pygame.rect.Rect((50, 50), (700, 500)), manager=gs.ui_manager)
    gs.console.hide()


def on_event(gs: GameState, e: Event):
    if e.type == pygame.KEYDOWN:
        if e.key == pygame.K_F1:
            gs.console.hide() if gs.console.visible == 1 else gs.console.show()

    if (e.type == pygame_gui.UI_CONSOLE_COMMAND_ENTERED and e.ui_element == gs.console):
        command = e.command
        print(command)
        gs.console.add_output_line_to_log("Hello!")


def draw(gs: GameState):
    pass
