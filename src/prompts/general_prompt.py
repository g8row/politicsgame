from animated_element import AnimatedElement, slerp

import state.game_state as GS
import state.ui_state as UI

from pygame.event import Event
import pygame
import pygame_gui as gui

from overrides import overrides

import traceback


class GeneralPrompt(AnimatedElement):
    #
    # Място за константи, които могат да се използват да се
    # разполагат UI елементите.
    #
    # Oпределят от изображението (GeneralPrompt.png за GeneralDialogueBox)
    #
    # Могат да се access-ват и от child class-ове.
    #
    DIM = 600, 499     # Целия размер на .png

    # Чистото място от прозореца
    USABLE_TOP_LEFT = (28, 43)
    USABLE_DIM = (545, 420)

    PADDING = 25     # Колко пиксела да има между ръбовете на prompt-а и нещата вътре
    ELEMENT_PADDING = 10     # ... същото, но между елементите вътре
    TOP_PADDING_BONUS = 20     # Отгоре има заглавие, което иначе много се бута ако не преместим нещата по-надолу

    # Синьото място горе за заглавие
    TITLE_TOP_LEFT = (200, 13)
    TITLE_DIM = (200, 54)

    # Колко да са големи самите UI елементи, хубаво е да са еднакви във всеки прозорец, за да има consistency
    BUTTON_DIM = (90, 50)

    container: gui.elements.UIPanel
    title: gui.elements.UILabel

    pre_code: str
    pre_code_ran: bool

    end_code: str
    end_code_ran: bool

    condition: str

    # Коя опция като индекс е избрал играча при скриване на prompt-а,
    # може да се access-не в end_code чрез "self.option",
    # но не винаги има смисъл... (напр. None е за prompt-ове без опции)
    option: int

    def __init__(self, object_id="#dialogue_box", dim=None):
        super().__init__()

        self.pre_code = ""
        self.pre_code_ran = False

        self.end_code = ""
        self.end_code_ran = False

        self.condition = ""

        if dim is None:
            dim = self.DIM

        self.container = gui.elements.UIPanel(
            relative_rect=center(UI.ui_manager.root_container, dim), starting_layer_height=10, manager=UI.ui_manager, object_id=object_id, visible=0
        )

        self.container_width = self.container.rect.width
        self.container_height = self.container.rect.height

        self.title = gui.elements.UILabel(
            relative_rect=pygame.Rect((0, 0), (-1, -1)),
            text="",
            manager=UI.ui_manager,
            container=self.container,
            object_id="#dialogue_box_title",
            visible=0
        )

    def on_show(self):
        pass

    def should_show(self) -> bool:
        evaluated: bool = True
        try:
            if len(self.condition):
                evaluated = eval(self.condition)
        except Exception:
            print(f"Грешка в condition \"{self.condition}\"")
            traceback.print_exc()
            evaluated = False

        return evaluated

    # Това се вика от state.ui_state, защото там е логиката за queue-ването!
    def show(self, animation: bool):
        self.container.show()
        self.on_show()

        if not self.pre_code_ran:
            self.pre_code_ran = True
            try:
                if len(self.pre_code):
                    exec(self.pre_code)
            except Exception:
                print(f"Грешка в pre_code \"{self.pre_code}\"")
                traceback.print_exc()

        if animation:
            self.container.disable()
            self.begin_alpha_animation(True)
        else:
            # Скипни анимацията.. (ако прозорчетата са били в queue)
            self.container.enable()
            self.skip_alpha_animation(True)

    # Това се вика от state.ui_state, защото там е логиката за queue-ването!
    def hide(self, animation: bool):
        if not self.end_code_ran:
            self.end_code_ran = True
            try:
                if len(self.end_code):
                    exec(self.end_code)
            except Exception:
                print(f"Грешка в end_code \"{self.end_code}\"")
                traceback.print_exc()

        if animation:
            UI.set_prompt_in_hide(self)
            self.container.disable()
            self.begin_alpha_animation(False)
        else:
            # Скипни анимацията.. (ако прозорчетата са били в queue)
            self.container.hide()
            self.skip_alpha_animation(False)

    def set_title(self, title: str):
        self.title.set_text(title)

        # Центрирай заглавието
        x, y = self.TITLE_TOP_LEFT
        w, h = self.TITLE_DIM
        x += w / 2
        y += h / 2
        x -= self.title.rect.width / 2
        y -= self.title.rect.height / 2
        self.title.set_relative_position((x, y))

    @overrides
    def on_t_changed(self, alpha: int, t: float):
        handle_alpha_for_element_and_its_children(self.container, alpha)

        anim_width = int(slerp(0.8 * self.container_width, self.container_width, t))
        anim_height = int(slerp(0.8 * self.container_height, self.container_height, t))

        self.container.rect.width = anim_width
        self.container.rect.width = anim_height

    def on_event(self, e: Event):
        pass

    @overrides
    def on_t_reached_1(self):
        self.container.enable()

    @overrides
    def on_t_reached_0(self):
        UI.prompt_done_hiding(self)


def center(container: gui.core.UIContainer, size: tuple[int | float, int | float]):
    x, y = container.rect.center
    w, h = size
    x -= w / 2
    y -= h / 2
    return pygame.Rect((x, y), (w, h))


def handle_alpha_for_element_and_its_children(root, alpha: int):
    if hasattr(root, "blendmode") and hasattr(root, "_image"):
        root.blendmode = 0
        root._image.set_alpha(alpha)

    if hasattr(root, "scrollbar"):
        handle_alpha_for_element_and_its_children(root.scroll_bar, alpha)

    if hasattr(root, "panel_container"):
        for e in root.panel_container.elements:
            handle_alpha_for_element_and_its_children(e, alpha)
