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
    # type       - коя картинка да покаже за края, има 4 типа засега: "good", "bad", "protest", "technology"
    def __init__(self, title: str = "", type: str = "", desc_html: str = "", condition: str = ""):
        super().__init__(f"#{type}_ending", (802, 602))
        self.set_title(title)
        
        x = self.title.rect.x - 8
        y = self.title.rect.y + 50
        w, h = (340, 80)

        self.desc = gui.elements.UITextBox(
            html_text=desc_html,
            relative_rect=pygame.Rect((0, 0), (w, h)),
            manager=UI.ui_manager,
            container=self.container,
            object_id=f"#ending_desc"
        )

        self.desc.set_relative_position((x, y))

        self.condition = condition
