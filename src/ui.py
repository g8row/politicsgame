from pygame.event import Event
from state import GameState
import pygame
import pygame_gui as gui

from typing import Tuple


def center(container: gui.core.UIContainer, size: Tuple[int | float, int | float]):
    x, y = container.rect.center
    w, h = size
    x -= w / 2
    y -= h / 2
    return pygame.Rect((x, y), (w, h))


def init(gs: GameState):
    gs.add_ui(
        gui.elements.UIPanel(
            relative_rect=center(gs.ui_manager.root_container, (369, 181)), starting_layer_height=10, manager=gs.ui_manager, object_id="#name_dialog"
        )
    )


def on_event(gs: GameState, e: Event):
    pass


def frame(gs: GameState):
    pass
