import pygame

from typing import Tuple

from state import GameState


def init(gs: GameState):
    gs.center = (gs.world_render_target.get_width() // 2, gs.world_render_target.get_height() // 2)
    gs.images["room"] = pygame.image.load("data/room/room.png")


def draw(gs: GameState):
    gs.world_render_target.fill("0xfff6d9")     # Едно хубаво жълтичко

    room = gs.images["room"]
    cx, cy = gs.center
    cx -= room.get_width() / 2
    cy -= room.get_height() / 2
    gs.world_render_target.blit(room, (cx, cy))
