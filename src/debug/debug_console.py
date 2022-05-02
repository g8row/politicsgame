from pygame.event import Event
import state.game_state as GS
import state.ui_state as UI

import pygame
import pygame_gui as gui


class DebugConsole:
    console: gui.windows.UIConsoleWindow

    def __init__(self):
        self.console = gui.windows.UIConsoleWindow(
            visible=0, rect=pygame.rect.Rect((50, 50), (500, 300)), manager=UI.debug_manager, object_id="#debug_console"
        )
        UI.add(self.console)

    def on_event(self, e: Event):
        console = self.console

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
                self.handle_set_command(args)
            elif tokens[0] == "modify_ui" or tokens[0] == "modui" or tokens[0] == "ui":
                self.handle_modify_ui_command(args)
            elif tokens[0] == "metrics":
                self.handle_metrics_command(args)
            elif tokens[0] == "marker":
                self.handle_marker_command(args)
            elif tokens[0] == "hammers":
                self.handle_hammers_command(args)
            else:
                console.add_output_line_to_log(f"Незнайна команда: '{tokens[0]}'")

    def handle_modify_ui_command(self, args: list[str]):
        console = self.console

        if len(args) < 1:
            console.add_output_line_to_log("'modify_ui' му трябва ID на UI обект, който да бара")
            return

        ui_id = args[0]
        if ui_id not in UI.elements:
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
            eval("UI.elements[ui_id]" + value)
        except Exception as exception:
            console.add_output_line_to_log(f"Имаше грешка при изпълнение: {exception}")

    def handle_set_command(self, args: list[str]):
        console = self.console

        if len(args) < 1:
            console.add_output_line_to_log("'set' му трябва име на променлива, която да презапише")
            return

        var_name = args[0]
        if var_name not in UI.variables:
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
                eval("UI.variables[var_name]." + value[2:])
            else:
                value = eval(value)
                UI.variables[var_name] = value

            console.add_output_line_to_log(f"Супер си, готово. Нова стойност: {UI.variables[var_name]}")

            # Някоя променлива може да е на UI-а нещ
            for _, v in UI.elements.items():
                v.rebuild()
        except Exception as exception:
            console.add_output_line_to_log(f"Имаше грешка при изпълнение: {exception}")

    def handle_metrics_command(self, args: list[str]):
        console = self.console

        if len(args) < 1:
            console.add_output_line_to_log("'metrics' му трябва режим (0 - disabled, 1 - само икономика, 2 - икономика и одобрение)")
            return

        mode = int(args[0])
        GS.metrics.set_mode(mode)

    def handle_marker_command(self, args: list[str]):
        console = self.console

        if len(args) < 2:
            console.add_output_line_to_log(
                "'marker' му трябва индекс (0 - икономика, 1 - одобрение) и стойност (число от 0 до 1, което представлява от 0% до 100%)"
            )
            return

        index = int(args[0])
        factor = float(args[1])

        GS.metrics.set_marker_percentage(index, factor)

    def handle_hammers_command(self, args: list[str]):
        console = self.console

        if len(args) < 1:
            console.add_output_line_to_log("'hammers' му трябва положително (или отрицателно) число, което казва колко чукчета да добави (или махне)")
            return

        hammers = int(args[0])
        GS.hammers.add_hammers(hammers)