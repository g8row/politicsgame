from collections import deque
import pygame_gui as gui
import room
import ui
import debug_ui
import state.game_state as GS
import state.ui_state as UI
import script
import sys
import time

# @Volatile: Всички възможни prompt-ове от script-а трябва да са import-нати тук и в script.py
from prompts.prompt_ask_for_identity import PromptAskForIdentity
from prompts.prompt_just_ok import PromptJustOk

import pygame


def main():
    pygame.init()

    win = pygame.display.set_mode(GS.win_size, pygame.DOUBLEBUF)     # Прозорец
    pygame.display.set_caption("res publica")     # Заглавие

    # Game state, всички могат да слагат (и махат) неща в тази променилива
    GS.win = win     # пример..., някои функции искат да имат прозореца
    GS.world_render_target = pygame.Surface((400, 300))

    UI.debug_manager = gui.UIManager(GS.win_size, "data/debug_ui_theme.json")
    UI.init_object_pools()

    target_fps = 60

    # Колко секунди трябва да продължава всеки фрейм (логика + рисуване), за да hit-нем target FPS-а
    GS.dt = 1 / target_fps

    # Колко наносекунди трябва да продължава всеки фрейм (логика + рисуване), за да hit-нем target FPS-а
    frame_time_ns = GS.dt * 10**9

    room.init()
    room.draw()

    debug_ui.init()
    ui.init()

    if not script.parse():
        return

    frame_time_stack = deque([])

    prev_time = time.time_ns()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            debug_ui.on_event(e)
            UI.debug_manager.process_events(e)

            ui.on_event(e)

        # Тук се случва цялата логика за всеки фрейм
        GS.win.blit(pygame.transform.scale(GS.world_render_target, (800, 600)), (0, 0))

        ui.frame()
        debug_ui.frame()

        UI.debug_manager.update(GS.dt)
        UI.debug_manager.draw_ui(GS.win)

        seconds_passed = GS.time_speed * GS.dt
        GS.time_in_game += seconds_passed

        GS.time_print_frame += 1
        if GS.time_print_frame % 60 == 0:
            print(f"Ден в игра: {int(GS.time_in_game / 4)}")

        current_day = int(GS.time_in_game / 4)
        if current_day in GS.script:
            for s in GS.script[current_day]:
                UI.prompt(eval(s))
            GS.script.pop(current_day)

        # Локва играта да рънва на 60 FPS вместо да точи процесора:
        curr_time = time.time_ns()
        diff = curr_time - prev_time
        prev_time = curr_time

        frame_time_stack.append(diff / 10**9)
        if len(frame_time_stack) > 2000:
            frame_time_stack.popleft()
        pygame.display.set_caption("res publica | {:.2f} FPS".format(1 / (sum(frame_time_stack) / len(frame_time_stack))))

        pygame.display.update()

        time.sleep(max(frame_time_ns - diff, 0) / 10**9)


if __name__ == "__main__":
    main()
