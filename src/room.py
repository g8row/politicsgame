import pygame

from typing import Tuple

import state.game_state as GS


def init():
    GS.center = (GS.world_render_target.get_width() // 2, GS.world_render_target.get_height() // 2)
    
    room = pygame.image.load("data/room/room.png")
    room = pygame.transform.scale(room, (room.get_size()[0] * 2, room.get_size()[1] * 2))
    GS.images["room"] = room


def frame():
    GS.world_render_target.fill("0xfff6d9")     # Едно хубаво жълтичко

    room = GS.images["room"]
    cx, cy = GS.center
    cx -= room.get_width() / 2
    cy -= room.get_height() / 2
    GS.world_render_target.blit(room, (cx, cy))
