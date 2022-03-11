import pygame_gui as gui
from debug.debug_console import DebugConsole

from typing import Any

#
# Глобални променливи,
#

# Неща за pygame_gui, set-ват се от main.py, нужни са,
# когато се прави нов UI element (параметъра manager),
# виж пример в prompt-овете.
manager: gui.UIManager
debug_manager: gui.UIManager

# Eлементи и променливи, които могат да се пипат от конзолата,
# може да се add-ват отвсякъде.
elements: dict[str, gui.core.UIElement] = {}
variables: dict[str, Any] = {}


def add(ui_obj: gui.core.UIElement):
    global elements

    id = ui_obj.object_ids[-1]
    print("Adding UI with ID:", id)
    elements[id] = ui_obj


def get(id: str) -> gui.core.UIElement | None:
    global elements

    return elements.get(id, None)


# Init-ва се от debug_ui.py
debug_console: DebugConsole

# Когато се извика prompt(), която да покаже нов прозорец, го слагаме в queue,
# защото играча може да не е затворил още първия.
# Ако няма видим прозорец в момента не се слага тук а директно се показва.
prompts_queue = []
active_prompt = None
prompt_in_hide = None     # Трябва да update-ваме prompt-а, който е в hide анимация, докато не се скрие на пълно


def prompt(p):
    global active_prompt

    if active_prompt is not None:
        prompts_queue.append(p)
    else:
        active_prompt = p
        p.show(animation=True)


def prompt_hide():
    global active_prompt
    global prompts_queue

    if active_prompt is not None:
        if len(prompts_queue) > 0:
            active_prompt.hide(animation=False)
            active_prompt = prompts_queue[0]
            prompts_queue = prompts_queue[1:]
            active_prompt.show(animation=False)
        else:
            active_prompt.hide(animation=True)
            active_prompt = None


def prompt_done_hiding(p):
    if prompt_in_hide == p:
        p.hide(animation=False)


def set_prompt_in_hide(p):
    global prompt_in_hide

    if prompt_in_hide is not None:
        # Скрий веднага стария, това ще се случи само ако по някакъв начин два prompt-а тръгват да се скриват по едно и също време. Тогава няма значение за този "отдолу", тъй като горния ще го скрива. Да не говорим, че почти никога няма да се случи играча да скрие втория по-бързо отколкото анимацията на първия. Въпреки това, ако се случи този невероятен случай, не трябва да оставяме стария prompt видим, защото като override-нем prompt_in_hide, той ще спира да се update-ва. Можем да го сложим в списък (нещо като prompts_in_hide), но няма нужда поради горе-описаното (просто не е нужно да е толкова точно, това е само edge case).
        p.hide(animation=False)

    prompt_in_hide = p
