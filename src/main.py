import pygame_gui as gui
import room
import ui
import debug_ui
import state.game_state as GS
import state.ui_state as UI
import sys
import time

import pygame

pygame.init()

win = pygame.display.set_mode(GS.win_size, pygame.DOUBLEBUF)     # Прозорец
pygame.display.set_caption("res publica")     # Заглавие

# Game state, всички могат да слагат (и махат) неща в тази променилива
GS.win = win     # пример..., някои функции искат да имат прозореца
GS.world_render_target = pygame.Surface((400, 300))

UI.debug_manager = gui.UIManager(GS.win_size, "data/debug_ui_theme.json")
# UI.manager = gui.UIManager(GS.win_size, "data/ui_theme.json")

target_fps = 60
# Колко наносекунди трябва да продължава всеки фрейм (логика + рисуване), за да hit-нем target FPS-а
frame_time_ns = 1.0 / target_fps * 10**9

room.init()
room.draw()

debug_ui.init()
ui.init()

prev_time = time.time_ns()
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()
        debug_ui.on_event(e)
        UI.debug_manager.process_events(e)

        ui.on_event(e)
        #UI.manager.process_events(e)

    # Тук се случва цялата логика за всеки фрейм
    GS.win.blit(pygame.transform.scale(GS.world_render_target, (800, 600)), (0, 0))

    ui.frame()
    debug_ui.frame()

    #UI.manager.update(1 / target_fps)
    #UI.manager.draw_ui(GS.win)

    UI.debug_manager.update(1 / target_fps)
    UI.debug_manager.draw_ui(GS.win)

    # Локва играта да рънва на 60 FPS вместо да точи процесора:
    curr_time = time.time_ns()
    diff = curr_time - prev_time
    prev_time = curr_time

    pygame.display.update()

    time.sleep(max(frame_time_ns - diff, 0) / 10**9)
