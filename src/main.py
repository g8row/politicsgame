import pygame_gui
import room
import ui
import debug_ui
import state
from types import SimpleNamespace
import sys
import time

import pygame
pygame.init()


win = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF)  # Прозорец
pygame.display.set_caption("res publica")                    # Заглавие

# Game state, всички могат да слагат (и махат) неща в тази променилива
gs = state.GameState()
gs.win = win            # пример..., някои функции искат да имат прозореца

gs.world_render_target = pygame.Surface((400, 300))
gs.debug_ui_manager = pygame_gui.UIManager(
    (800, 600), "data/debug_ui_theme.json")
gs.ui_manager = pygame_gui.UIManager((800, 600), "data/ui_theme.json")

target_fps = 60
# Колко наносекунди трябва да продължава всеки фрейм (логика + рисуване), за да hit-нем target FPS-а
frame_time_ns = 1.0 / target_fps * 10 ** 9

room.init(gs)
debug_ui.init(gs)
ui.init(gs)

prev_time = time.time_ns()
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()
        debug_ui.on_event(gs, e)
        gs.debug_ui_manager.process_events(e)

        ui.on_event(gs, e)
        gs.ui_manager.process_events(e)

    gs.world_render_target.fill("0xfff6d9")  # Едно хубаво жълтичко

    # Тук се случва цялата логика за всеки фрейм
    room.draw(gs)
    ui.draw(gs)
    debug_ui.draw(gs)

    gs.win.blit(pygame.transform.scale(
        gs.world_render_target, (800, 600)), (0, 0))

    gs.ui_manager.update(1 / target_fps)
    gs.ui_manager.draw_ui(gs.win)

    gs.debug_ui_manager.update(1 / target_fps)
    gs.debug_ui_manager.draw_ui(gs.win)

    # Локва играта да рънва на 60 FPS вместо да точи процесора:
    curr_time = time.time_ns()
    diff = curr_time - prev_time
    prev_time = curr_time

    pygame.display.flip()

    time.sleep(max(frame_time_ns - diff, 0) / 10 ** 9)
