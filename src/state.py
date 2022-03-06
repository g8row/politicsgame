import pygame
import pygame
import pygame_gui as gui

from typing import Any, Dict, Tuple

from collections import defaultdict


class GameState:
    win: pygame.surface.Surface

    world_render_target: pygame.surface.Surface
    center: Tuple[int, int]

    images: dict[str, pygame.surface.Surface] = {}

    ui_manager: gui.UIManager
    debug_ui_manager: gui.UIManager

    ui_elements: Dict[str, gui.core.UIElement] = {}

    def add_ui(self, id: str, object: gui.core.UIElement):
        object.object_ids.append(id)
        self.ui_elements[id] = object

    def get_ui(self, id: str) -> gui.core.UIElement | None:
        return self.ui_elements.get(id, None)

    variables: Dict[str, Any] = {}
