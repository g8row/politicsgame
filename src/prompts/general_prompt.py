import math
from animated_element import AnimatedElement

import state.game_state as GS
import state.ui_state as UI

from pygame.event import Event
import pygame
import pygame_gui as gui


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
    TEXT_ENTRY_DIM = (130, 25)

    # Самото геройче дето излиза в началото на играта, когато те пита за името
    CHARACTER_DIM = (80, 110)

    title: gui.elements.UILabel

    def __init__(self):
        super().__init__()

        # Всеки, който наследява AnimatedElement трябва да set-не това,
        # но не може да го pass-нем в constructor-а, защото ни трябва
        # self.manager, което се init-ва от там...
        self.container = gui.elements.UIPanel(
            relative_rect=center(self.manager.root_container, self.DIM),
            starting_layer_height=10,
            manager=self.manager,
            object_id="#dialogue_box",
            visible=0
        )

        self.title = gui.elements.UILabel(
            relative_rect=pygame.Rect((0, 0), (-1, -1)),
            text="",
            manager=self.manager,
            container=self.container,
            object_id="#dialogue_box_title",
            visible=0
        )

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


def center(container: gui.core.UIContainer, size: tuple[int | float, int | float]):
    x, y = container.rect.center
    w, h = size
    x -= w / 2
    y -= h / 2
    return pygame.Rect((x, y), (w, h))
