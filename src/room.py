import pygame

from typing import Tuple

from state import GameState


def init(gs: GameState):
    gs.center = (gs.world_render_target.get_width() // 2,
                 gs.world_render_target.get_height() // 2)
    gs.images["room"] = pygame.image.load("data/room/room.png")


def draw(gs: GameState):
    room = gs.images["room"]
    cx, cy = gs.center

    # Центрирай стаята
    cx -= room.get_width() / 2
    cy -= room.get_height() / 2
    gs.world_render_target.blit(room, (cx, cy))
