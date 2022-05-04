from prompts.general_prompt import GeneralPrompt

import state.ui_state as UI

from pygame.event import Event
import pygame
import pygame_gui as gui

from overrides import overrides


#
# Прозорче със заглавие и текст (въпрос) и колкото искаш на брой отговори.
# Всеки отговор има индекс (от 0 до n-1) и set-ва self.option в GeneralPrompt.
# В end_code може да се access-не индекса на отговора, който е даден.
#
class PromptQuestion(GeneralPrompt):
    OPTION_DIM = (500, 30)
    OPTION_PADDING = 5

    title: gui.elements.UILabel
    desc: gui.elements.UITextBox

    desc_to_show_next_frames: int = 0
    desc_text_to_show: str

    buttons: dict[gui.elements.UIButton, int] = {}

    # title      - oбикновен string; това, което се показва
    #              горе в синьото правоъгълниче
    # desc_html  - текстът, който има анимация на изписване,
    #              може да има html в него (style-ване, bold, italic и т.н.)
    def __init__(
        self,
        title: str = "",
        desc_html: str = "",
        pre_code: str = "",
        end_code: str = "",
        options_html: list[str] = ["1", "2", "3"],
        condition: str = ""
    ):
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

        option_width, option_height = self.OPTION_DIM

        dy += option_height
        dy += self.PADDING

        self.desc = gui.elements.UITextBox(
            html_text="",
            relative_rect=pygame.Rect((x, y), (w, h - self.OPTION_PADDING - len(options_html) * (option_height + self.OPTION_PADDING))),
            manager=UI.ui_manager,
            container=self.container,
            object_id="#dialogue_box_desc",
            visible=0
        )

        self.desc_to_show_next_frames = 1
        self.desc_text_to_show = desc_html

        index = len(options_html) - 1

        for o in reversed(options_html):
            button = gui.elements.UIButton(
                relative_rect=pygame.Rect((x + (w - option_width) / 2, -dy), self.OPTION_DIM),
                text=o,
                manager=UI.ui_manager,
                container=self.container,
                object_id="#question_option_button",
                visible=0,
                anchors={
                    "top": "bottom",
                    "left": "left",
                    "bottom": "bottom",
                    "right": "left"
                }
            )

            self.buttons[button] = index
            index -= 1

            dy += option_height + self.OPTION_PADDING

        self.condition = condition
        self.pre_code = pre_code
        self.end_code = end_code

    @overrides
    def on_show(self):
        self.desc.hide()

    @overrides
    def frame(self):
        super().frame()

        # Това е хак, защото pygame_gui има лек бъг с text typing ефекта..
        # Държим текста невидим за (поне) 5 фрейма докато не почне да пише първата буква,
        # иначе има лек период, в който е видимо цялото описание.
        if self.desc_to_show_next_frames == 1:
            self.desc.set_text(self.desc_text_to_show)
            self.desc.set_active_effect(gui.TEXT_EFFECT_TYPING_APPEAR, params={"time_per_letter": 0.00001})
        if self.desc_to_show_next_frames == 6:
            self.desc.show()
            self.desc_to_show_next_frames = 0
        if self.desc_to_show_next_frames != 0:
            self.desc_to_show_next_frames += 1

    @overrides
    def on_event(self, e: Event):
        super().on_event(e)

        # Играча цъка бутона...
        if e.type == gui.UI_BUTTON_PRESSED:
            if e.ui_element in self.buttons:
                self.option = self.buttons[e.ui_element]     # Отбележи индекса на избрания отговор...
                print("Option:", self.option)
                UI.prompt_hide()     # Не скривай директно! Има логика за queue-ване в state.ui_state...

        # Играча цъка текста, който се изписва, тук забързваме анимацията
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == pygame.BUTTON_LEFT:
            mx, my = pygame.mouse.get_pos()
            if self.desc.rect.collidepoint((mx, my)):
                if self.desc.active_text_effect is not None:
                    self.desc.active_text_effect.time_per_letter = 0.000005