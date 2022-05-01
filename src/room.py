import pygame

from typing import Tuple

import state.game_state as GS


def init():
    GS.center = (GS.win_size[0] // 2, GS.win_size[1] // 2)

    room = pygame.image.load("data/room/room.png")
    room = pygame.transform.scale(room, (room.get_width() * 2, room.get_height() * 2))
    GS.images["room"] = room


def frame():
    room = GS.images["room"]
    cx, cy = GS.center
    cx -= room.get_width() / 2
    cy -= room.get_height() / 2
    GS.win_surface.blit(room, (cx, cy))
