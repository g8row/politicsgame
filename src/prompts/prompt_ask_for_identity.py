from prompts.general_prompt import GeneralPrompt

import state.ui_state as UI

from pygame.event import Event
import pygame
import pygame_gui as gui

from overrides import overrides


#
# Прозорчето в началото, което пита за името на играча и т.н.
#
class PromptAskForIdentity(GeneralPrompt):
    TEXT_ENTRY_DIM = (130, 25)
    CHARACTER_DIM = (80, 110)

    ok_button: gui.elements.UIButton

    name_entry: gui.elements.UITextEntryLine
    gender_list: gui.elements.UISelectionList
    character: gui.elements.UIImage

    def __init__(self):
        super().__init__()
        self.set_title("Вие сте...")

        ux, uy = self.USABLE_TOP_LEFT
        uw, uh = self.USABLE_DIM

        x, y = ux, uy
        w, h = uw, uh

        x += self.PADDING
        y += self.PADDING + self.TOP_PADDING_BONUS

        w -= self.PADDING * 2
        h -= self.PADDING * 2 + self.TOP_PADDING_BONUS

        tw, th = self.DIM
        dy = th - (uy + uh)

        button_width, button_height = self.BUTTON_DIM

        dy += button_height
        dy += self.PADDING

        self.ok_button = gui.elements.UIButton(
            relative_rect=pygame.Rect((x + (w - button_width) / 2, -dy), self.BUTTON_DIM),
            text="Добре",
            manager=UI.ui_manager,
            container=self.container,
            object_id="#dialogue_box_ok_button",
            visible=0,
            anchors={
                'top': 'bottom',
                'left': 'left',
                'bottom': 'bottom',
                'right': 'left'
            }
        )

        self.name_entry = gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((x, y), (w, button_height)),
            manager=UI.ui_manager,
            container=self.container,
            object_id="#dialogue_box_textentry",
            visible=0
        )
        self.name_entry.set_text("Име...")

        gender_list_width, gender_list_height = self.TEXT_ENTRY_DIM

        self.gender_list = gui.elements.UIDropDownMenu(
            relative_rect=pygame.Rect((x + (w - gender_list_width) / 2, self.ELEMENT_PADDING + 10), self.TEXT_ENTRY_DIM),
            options_list=["Жена", "Небинарен", "Мъж"],
            starting_option="Жена",
            manager=UI.ui_manager,
            container=self.container,
            object_id="#dialogue_box_genderlist",
            visible=0,
            anchors={
                'top': 'top',
                'left': 'left',
                'bottom': 'top',
                'right': 'left',
                'top_target': self.name_entry
            }
        )

        character_width, character_height = self.CHARACTER_DIM

        self.character = gui.elements.UIImage(
            relative_rect=pygame.Rect((x + (w - character_width) / 2, self.ELEMENT_PADDING + 35), self.CHARACTER_DIM),
            image_surface=pygame.transform.scale(pygame.image.load("data/character.png"), self.CHARACTER_DIM),
            manager=UI.ui_manager,
            container=self.container,
            object_id="#dialogue_box_character",
            visible=0,
            anchors={
                'top': 'top',
                'left': 'left',
                'bottom': 'top',
                'right': 'left',
                'top_target': self.gender_list
            }
        )

    @overrides
    def on_event(self, e: Event):
        super().on_event(e)

        # Играча цъка бутона...
        if e.type == gui.UI_BUTTON_PRESSED:
            if e.ui_element == self.ok_button:
                UI.prompt_hide()     # Не скривай директно! Има логика за queue-ване в state.ui_state...

        # Изтрий първоначалния текст, когато играча тръгне да пише, иначе "Име..." си стои..
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == pygame.BUTTON_LEFT:
            mx, my = pygame.mouse.get_pos()
            if self.name_entry.rect.collidepoint((mx, my)):
                if self.name_entry.text is not None and self.name_entry.text == "Име...":
                    self.name_entry.set_text("")