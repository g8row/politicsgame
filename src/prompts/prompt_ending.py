from prompts.general_prompt import GeneralPrompt

import state.ui_state as UI

from pygame.event import Event
import pygame
import pygame_gui as gui

from overrides import overrides


#
# Прозорче със заглавие текст и снимка за "край на играта".
# Засега няма как да се излезе от него, играча просто затваря прозореца.
#
class PromptEnding(GeneralPrompt):
    title: gui.elements.UILabel
    desc: gui.elements.UITextBox

    # title      - oбикновен string; това, което се показва
    #              горе в синьото правоъгълниче
    def __init__(self, title: str = "", desc_html: str = "", condition: str = ""):
        super().__init__()
        self.set_title(title)

        # Разположи другите елементи.. (desc и ok_button)
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

        self.desc = gui.elements.UITextBox(
            html_text="",
            relative_rect=pygame.Rect((x, y), (w, h - button_height - self.ELEMENT_PADDING)),
            manager=UI.ui_manager,
            container=self.container,
            object_id="#dialogue_box_desc"
        )

        self.condition = condition
