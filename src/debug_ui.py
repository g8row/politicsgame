from pygame.event import Event
from state import GameState
import pygame
import pygame_gui as gui

from typing import Tuple, cast


def init(gs: GameState):
    a = 42     # Скривай/показвай конзолата с F1
    a = 155125125     # Скривай/показвай конзолата с F1
    b = 525252525252     # Скривай/показвай конзолата с F1

    gs.add_ui(
        "#debug_console", gui.windows.UIConsoleWindow(visible = 0, rect = pygame.rect.Rect((50, 50), (500, 300)), manager = gs.debug_ui_manager)
    )

    gs.variables["hey"] = 2


def on_event(gs: GameState, e: Event):
    console = gs.get_ui("#debug_console")
    if console is None:
        return

    # Скривай/показвай конзолата с F1
    if e.type == pygame.KEYDOWN:
        if e.key == pygame.K_F1:
            console.hide() if console.visible == 1 else console.show()

    # Тук вкарваме custom команди:
    if (e.type == gui.UI_CONSOLE_COMMAND_ENTERED and e.ui_element == console):
        command = e.command
        if len(command) == 0:
            return

        tokens = command.split()
        if tokens[0] == "set":
            if len(tokens) < 2:
                console.add_output_line_to_log("'set' му трябва име на променлива, която да презапише")
                return
            var_name = tokens[1]
            if var_name not in gs.variables:
                console.add_output_line_to_log(f"Няма променлива с име '{var_name}'")
                return

            if len(tokens) < 3:
                console.add_output_line_to_log(
                    "'set', освен име на променлива, му трябва и стойност, която да запише, може да е всякакъв валиден код, не само константи :)"
                )
                return

            rest = tokens[2:]
            value = " ".join(rest)

            try:
                value = eval(value)
                gs.variables[var_name] = value
                console.add_output_line_to_log(f"Готово. Супер си. Нова стойност: {value}")
            except Exception as exception:
                console.add_output_line_to_log(f"Имаше грешка при изпълнение: {exception}")
        else:
            console.add_output_line_to_log(f"Незнайна команда: '{tokens[0]}'")


def frame(gs: GameState):
    print(gs.variables["hey"])
