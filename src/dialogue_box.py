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


def cubic_bezier(t: float, p0: float, p1: float, p2: float, p3: float) -> float:
    return (1.0 - t)**3 * p0 + 3 * (1.0 - t)**2 * t * p1 + 3 * (1.0 - t) * t**2 * p2 + t**3 * p3


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
    GENDERLIST_DIM = (130, 25)
    CHARACTER_DIM = (80, 110)

    panel: gui.elements.UIPanel
    title: gui.elements.UILabel
    desc: gui.elements.UITextBox
    textentry: gui.elements.UITextEntryLine
    okbutton: gui.elements.UIButton
    genderlist: gui.elements.UISelectionList
    character: gui.elements.UIImage

    queue = []

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
        self.desc_to_show_next_frames = 1

    def prompt(self, type: DialogueBoxType, title: str, desc_html: str):
        if self.panel.visible == 0:
            self._actually_prompt(type, title, desc_html)
        else:
            self.queue.append((type, title, desc_html))

    def _actually_prompt(self, type: DialogueBoxType, title: str, desc_html: str):
        self.panel.show()
        self.set_title(title)

        if type == DialogueBoxType.ASK_FOR_IDENTITY:
            desc_height_diff = (self.BUTTON_DIM[1] + self.ELEMENT_PADDING) * 2
            self.textentry.show()
            self.genderlist.show()
            self.character.show()
            self.desc.hide()
            return

        desc_height_diff = 0
        if type == DialogueBoxType.JUST_OK:
            desc_height_diff = self.BUTTON_DIM[1] + self.ELEMENT_PADDING
            self.textentry.hide()
            self.genderlist.hide()
            self.character.hide()

        self.desc.set_dimensions((self.desc.rect.width, self.USABLE_HEIGHT_AFTER_PADDING - desc_height_diff))
        self.set_desc(desc_html)

    def hide(self):
        if len(self.queue) == 0:
            self.panel.hide()
        else:
            self._actually_prompt(*self.queue[0])
            self.queue = self.queue[1:]

    def frame(self):
        # Това е хак, защото pygame_gui има лек бъг с text typing ефекта..
        # Държим текста невидим за 5 фрейма докато не почне да пише първата буква,
        # иначе има лек период, в който е видимо цялото описание.
        if self.desc_to_show_next_frames == 5:
            self.desc.show()
            self.desc_to_show_next_frames = 0
        if self.desc_to_show_next_frames != 0:
            self.desc_to_show_next_frames += 1

    def on_event(self, e: Event):
        if e.type == gui.UI_BUTTON_PRESSED:
            if e.ui_element == self.okbutton:
                self.hide()
                       
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == pygame.BUTTON_LEFT:
            mx, my = pygame.mouse.get_pos()
            if self.desc.rect.collidepoint((mx, my)):
                if self.desc.active_text_effect is not None:
                    self.desc.active_text_effect.time_per_letter = 0.00001

            if self.textentry.rect.collidepoint((mx, my)):
                if self.textentry.text is not None and self.textentry.text == "Име...":
                    self.textentry.set_text("")


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
            relative_rect=pygame.Rect((x + (w - button_width) / 2, -dy), self.BUTTON_DIM),
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
            relative_rect=pygame.Rect((x, y), (w, button_height)),
            manager=ui_manager,
            container=self.panel,
            object_id="#dialogue_box_textentry",
            visible=0
        )
        self.textentry.set_text("Име...")

        genderlist_width, genderlist_height = self.GENDERLIST_DIM

        self.genderlist = gui.elements.UIDropDownMenu(
            relative_rect=pygame.Rect((x + (w - genderlist_width) / 2, self.ELEMENT_PADDING + 10), self.GENDERLIST_DIM),
            options_list=["Жена", "Небинарен", "Мъж"],
            starting_option="Жена",
            manager=ui_manager,
            container=self.panel,
            object_id="#dialogue_box_genderlist",
            visible=0,
            anchors={
                'top': 'top',
                'left': 'left',
                'bottom': 'top',
                'right': 'left',
                'top_target': self.textentry
            }
        )

        character_width, character_height = self.CHARACTER_DIM

        self.character = gui.elements.UIImage(
            relative_rect=pygame.Rect((x + (w - character_width) / 2, self.ELEMENT_PADDING + 35), self.CHARACTER_DIM),
            image_surface=pygame.transform.scale(pygame.image.load("data/character.png"), self.CHARACTER_DIM),
            manager=ui_manager,
            container=self.panel,
            object_id="#dialogue_box_character",
            visible=0,
            anchors={
                'top': 'top',
                'left': 'left',
                'bottom': 'top',
                'right': 'left',
                'top_target': self.genderlist
            }
        )

        self.desc = gui.elements.UITextBox(
            html_text="", relative_rect=pygame.Rect((x, y), (w, h)), manager=ui_manager, container=self.panel, object_id="#dialogue_box_desc"
        )
