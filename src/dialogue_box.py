import pygame
import pygame_gui as gui

from pygame.event import Event

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

    PADDING = 25     # Между ръбовете на prompt-а
    ELEMENT_PADDING = 10     # Между елементите вътре
    TOP_PADDING_BONUS = 20

    # Синьото място за заглавие
    TITLE_TOP_LEFT = (200, 13)
    TITLE_DIM = (200, 54)

    USABLE_HEIGHT_AFTER_PADDING: int

    BUTTON_DIM = (90, 50)

    panel: gui.elements.UIPanel
    title: gui.elements.UILabel
    desc: gui.elements.UITextBox
    textentry: gui.elements.UITextEntryLine
    okbutton: gui.elements.UIButton

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
        self.desc.hide()
        self.to_show_next_frame = 1

    def prompt(self, type: DialogueBoxType, title: str, desc_html: str):
        self.panel.show()
        self.panel.enable()
        self.set_title(title)
        self.desc.hide()

        desc_height_diff = 0
        if type == DialogueBoxType.ASK_FOR_IDENTITY:
            desc_height_diff = self.BUTTON_DIM[1] + self.ELEMENT_PADDING
            self.textentry.hide()

        self.desc.set_dimensions((self.desc.rect.width, self.USABLE_HEIGHT_AFTER_PADDING - desc_height_diff))
        self.set_desc(desc_html)

    def hide(self):
        self.panel.hide()
        self.desc.set_text("")
        self.desc.set_active_effect(None)

    def frame(self):
        if self.to_show_next_frame == 5:
            self.desc.show()
            self.to_show_next_frame = 0
        if self.to_show_next_frame != 0:
            self.to_show_next_frame += 1

    def on_event(self, e: Event):
        if e.type == gui.UI_BUTTON_PRESSED:
            if e.ui_element == self.okbutton:
                print("Ok!")
                self.panel.disable()

    def __init__(self, ui_manager: gui.UIManager):
        self.panel = gui.elements.UIPanel(
            relative_rect=center(ui_manager.root_container, self.DIM),
            starting_layer_height=10,
            manager=ui_manager,
            object_id="#dialogue_box",
            visible=0
        )

        self.title = gui.elements.UILabel(
            relative_rect=pygame.Rect((0, 0), (-1, -1)),
            text="",
            manager=ui_manager,
            container=self.panel,
            object_id="#dialogue_box_title",
            visible=0
        )

        ux, uy = self.USABLE_TOP_LEFT
        uw, uh = self.USABLE_DIM

        x, y = ux, uy
        w, h = uw, uh

        x += self.PADDING
        y += self.PADDING + self.TOP_PADDING_BONUS

        w -= self.PADDING * 2
        h -= self.PADDING * 2 + self.TOP_PADDING_BONUS

        self.USABLE_HEIGHT_AFTER_PADDING = h

        tw, th = self.DIM
        dy = th - (uy + uh)

        button_width, button_height = self.BUTTON_DIM

        dy += button_height
        dy += self.PADDING

        self.okbutton = gui.elements.UIButton(
            relative_rect=pygame.Rect((x + (w - button_width) / 2, -dy), (button_width, button_height)),
            text="Добре",
            manager=ui_manager,
            container=self.panel,
            object_id="#dialogue_box_okbutton",
            visible=0,
            anchors={
                'top': 'bottom',
                'left': 'left',
                'bottom': 'bottom',
                'right': 'left'
            }
        )

        self.textentry = gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((x, -dy), (w, button_height)),
            manager=ui_manager,
            container=self.panel,
            object_id="#dialogue_box_textentry",
            visible=0,
            anchors={
                'top': 'bottom',
                'left': 'left',
                'bottom': 'bottom',
                'right': 'left'
            }
        )
        self.textentry.set_text("Име...")

        self.desc = gui.elements.UITextBox(
            html_text="", relative_rect=pygame.Rect((x, y), (w, h)), manager=ui_manager, container=self.panel, object_id="#dialogue_box_desc"
        )
