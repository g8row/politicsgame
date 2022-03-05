import pygame
import pygame
import pygame_gui

from typing import Tuple


class GameState:
    win: pygame.surface.Surface

    center: Tuple[int, int]
    images: dict[str, pygame.surface.Surface] = {}

    world_render_target: pygame.surface.Surface

    debug_ui_manager: pygame_gui.UIManager
    ui_manager: pygame_gui.UIManager

    console = pygame_gui.windows.UIConsoleWindow
