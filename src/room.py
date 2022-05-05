import pygame

from typing import Tuple

import state.game_state as GS


def init():
    GS.center = (GS.win_size[0] // 2, GS.win_size[1] // 2)


def set_room(gender: str):
    if gender == "Жена":
        room = pygame.image.load("data/room/new/room_female.png")
    elif gender == "Мъж":
        room = pygame.image.load("data/room/new/room_male.png")
    else:
        room = pygame.image.load("data/room/new/room_nonbinary.png")

    room = pygame.transform.scale(room, (room.get_width() * 0.8, room.get_height() * 0.8))
    GS.images["room"] = room


def frame():
    if "room" not in GS.images:
        return     # Не е сетната още

    room = GS.images["room"]
    cx, cy = GS.center
    cx -= room.get_width() / 2
    cy -= room.get_height() / 2
    GS.win_surface.blit(room, (cx, cy))
