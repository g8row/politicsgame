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

    def add_ui(self, ui_obj: gui.core.UIElement):
        id = ui_obj.object_ids[0]
        print("Adding UI with ID:", id)
        self.ui_elements[id] = ui_obj

    def get_ui(self, id: str) -> gui.core.UIElement | None:
        return self.ui_elements.get(id, None)

    variables: Dict[str, Any] = {}
