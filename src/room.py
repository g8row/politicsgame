import pygame

from typing import Tuple

import state.game_state as GS


def init():
    GS.center = (GS.world_render_target.get_width() // 2, GS.world_render_target.get_height() // 2)
    GS.images["room"] = pygame.image.load("data/room/room.png")


def draw():
    GS.world_render_target.fill("0xfff6d9")     # Едно хубаво жълтичко

    room = GS.images["room"]
    cx, cy = GS.center
    cx -= room.get_width() / 2
    cy -= room.get_height() / 2
    GS.world_render_target.blit(room, (cx, cy))
