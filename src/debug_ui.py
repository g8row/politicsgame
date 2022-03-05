from pygame.event import Event
from state import GameState
import pygame
import pygame_gui

from typing import Tuple


def init(gs: GameState):
    gs.console = pygame_gui.windows.UIConsoleWindow(
        rect=pygame.rect.Rect((50, 50), (700, 500)), manager=gs.debug_ui_manager, object_id="#console")
    gs.console.hide()
    print(gs.console.combined_element_ids)

def on_event(gs: GameState, e: Event):
    # Скривай/показвай конзолата с F1
    if e.type == pygame.KEYDOWN:
        if e.key == pygame.K_F1:
            gs.console.hide() if gs.console.visible == 1 else gs.console.show()

    # Тук вкарваме custom команди: 
    if (e.type == pygame_gui.UI_CONSOLE_COMMAND_ENTERED and e.ui_element == gs.console):
        command = e.command
        print(command)   # За сега не хендълваме нищо
 

def draw(gs: GameState):
    pass
