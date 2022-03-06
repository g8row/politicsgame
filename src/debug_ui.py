from pygame.event import Event
from state import GameState
import pygame
import pygame_gui as gui

from typing import List


def init(gs: GameState):
    gs.add_ui(
        gui.windows.UIConsoleWindow(visible=0, rect=pygame.rect.Rect((50, 50), (500, 300)), manager=gs.debug_ui_manager, object_id="#debug_console")
    )

    gs.debug_ui_manager.ui_group


def on_event(gs: GameState, e: Event):
    console = gs.get_ui("#debug_console")
    if console is None:
        return

    # Скривай/показвай конзолата с F1
    if e.type == pygame.KEYDOWN:
        if e.key == pygame.K_F1:
            console.hide() if console.visible == 1 else console.show()

    # Тук вкарваме custom команди:
    if e.type == gui.UI_CONSOLE_COMMAND_ENTERED and e.ui_element == console:
        command = e.command
        if len(command) == 0:
            return

        tokens = command.split()

        args = []
        if len(tokens) > 0:
            args = tokens[1:]

        if tokens[0] == "set":
            handle_set_command(gs, console, args)
        elif tokens[0] == "modify_ui" or tokens[0] == "modui" or tokens[0] == "ui":
            handle_modify_ui_command(gs, console, args)
        else:
            console.add_output_line_to_log(f"Незнайна команда: '{tokens[0]}'")


def handle_modify_ui_command(gs: GameState, console: gui.windows.UIConsoleWindow, args: List[str]):
    if len(args) < 1:
        console.add_output_line_to_log("'modify_ui' му трябва ID на UI обект, който да бара")
        return

    ui_id = args[0]
    if ui_id not in gs.ui_elements:
        console.add_output_line_to_log(f"Няма UI с ID '{ui_id}'")
        return

    if len(args) < 2:
        console.add_output_line_to_log(
            "'modify_ui' му трябва и код, който да изпълни на обекта; пр. 'modify_ui #name_dialog .set_dimensions((100, 200))'"
        )
        return

    rest = args[1:]
    value = " ".join(rest)

    if value[0] != '.':
        console.add_output_line_to_log(
            "'modify_ui' му трябва код, който да започва с точка; пр. 'modify_ui #name_dialog .set_dimensions((100, 200))'"
        )
        return

    try:
        eval("gs.ui_elements[ui_id]" + value)
    except Exception as exception:
        console.add_output_line_to_log(f"Имаше грешка при изпълнение: {exception}")


def handle_set_command(gs: GameState, console: gui.windows.UIConsoleWindow, args: List[str]):
    if len(args) < 1:
        console.add_output_line_to_log("'set' му трябва име на променлива, която да презапише")
        return

    var_name = args[0]
    if var_name not in gs.variables:
        console.add_output_line_to_log(f"Няма променлива с име '{var_name}'")
        return

    if len(args) < 2:
        console.add_output_line_to_log(
            "'set', освен име на променлива, му трябва и стойност, която да запише, може да е всякакъв валиден код, не само константи :)"
        )
        return

    rest = args[1:]
    value = " ".join(rest)

    try:
        if value[0:2] == "_.":
            # Не презаписвай цялата, а вместо това интерпретирай като презаписване на някакво проперти, пр. _.width = 2, значи 'вземи старата и промени само width-а'
            eval("gs.variables[var_name]." + value[2:])
        else:
            value = eval(value)
            gs.variables[var_name] = value

        console.add_output_line_to_log(f"Супер си, готово. Нова стойност: {gs.variables[var_name]}")

        # Някоя променлива може да е на UI-а нещ
        for _, v in gs.ui_elements.items():
            v.rebuild()
    except Exception as exception:
        console.add_output_line_to_log(f"Имаше грешка при изпълнение: {exception}")


def frame(gs: GameState):
    pass
