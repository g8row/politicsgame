import pygame
import pygame_gui as gui

from enum import Enum


def center(container: gui.core.UIContainer, size: tuple[int | float, int | float]):
    x, y = container.rect.center
    w, h = size
    x -= w / 2
    y -= h / 2
    return pygame.Rect((x, y), (w, h))


class DialogueBoxType(Enum):
    ASK_FOR_IDENTITY = 0,
    JUST_OK = 1,     # Not implemented
    YES_NO = 2,     # Not implemented
    MULTIPLE_CHOICE = 3     # Not implemented


class DialogueBox:
    # Тези се определят от изображението (GeneralPrompt.png)
    DIM = 600, 499

    # Чистото място от прозореца
    USABLE_TOP_LEFT = (28, 43)
    USABLE_DIM = (545, 420)

    PADDING = 25
    TOP_PADDING_BONUS = 20

    # Синьото място за заглавие
    TITLE_TOP_LEFT = (200, 13)
    TITLE_DIM = (200, 54)

    panel: gui.elements.UIPanel
    title: gui.elements.UILabel
    desc: gui.elements.UITextBox

    def set_title(self, text: str):
        self.title.set_text(text)

        x, y = self.TITLE_TOP_LEFT
        w, h = self.TITLE_DIM
        x += w / 2
        y += h / 2
        x -= self.title.rect.width / 2
        y -= self.title.rect.height / 2
        self.title.set_relative_position((x, y))

    def set_desc(self, html_text: str):
        self.desc.set_text(html_text)
        self.desc.set_active_effect(gui.TEXT_EFFECT_TYPING_APPEAR, params={"time_per_letter": 0.05})

    def prompt(self, type: DialogueBoxType, title: str, desc_html: str):
        self.panel.show()
        pass

    def hide(self):
        self.panel.hide()

    def __init__(self, ui_manager: gui.UIManager):
        self.panel = gui.elements.UIPanel(
            relative_rect=center(ui_manager.root_container, self.DIM), starting_layer_height=10, manager=ui_manager, object_id="#dialogue_box"
        )

        self.title = gui.elements.UILabel(
            relative_rect=pygame.Rect((0, 0), (-1, -1)), text="", manager=ui_manager, container=self.panel, object_id="#dialogue_box_title"
        )

        ux, uy = self.USABLE_TOP_LEFT
        uw, uh = self.USABLE_DIM

        x, y = ux, uy
        w, h = uw, uh

        x += self.PADDING
        y += self.PADDING + self.TOP_PADDING_BONUS

        w -= self.PADDING * 2
        h -= self.PADDING * 2 + self.TOP_PADDING_BONUS

        self.desc = gui.elements.UITextBox(
            html_text="",
            relative_rect=pygame.Rect((x, y), (w, h)),
            manager=ui_manager,
            container=self.panel,
            object_id="#dialogue_box_desc",
            anchors={
                'left': 'left',
                'right': 'right',
                'top': 'top',
                'bottom': 'bottom'
            }
        )

        #name_dialog_textentry = gui.elements.UITextEntryLine(
        #    relative_rect=pygame.Rect((50, 373), (150, 50)), manager=gs.ui_manager, container=self.#panel, object_id="dialogue_box_textentry"
        #)
        #name_dialog_textentry.set_text("Име")

        #gs.add_ui(self.panel)
        #gs.add_ui(self.title)
        #gs.add_ui(self.desc)
        #gs.add_ui(name_dialog_textentry)
