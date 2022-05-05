from pygame.event import Event
import state.ui_state as UI

import pygame
import pygame_gui as gui


class Hammers():
    amount: int

    def __init__(self):
        self.amount = 1

        hammers_rect = pygame.Rect(0, 0, 141, 51)
        hammers_rect.topleft = (20, 20)

        hammers = gui.elements.UIPanel(relative_rect=hammers_rect, starting_layer_height=1, manager=UI.ui_manager, object_id="#hammers", visible=0)

        hammers_text_rect = pygame.Rect(0, 0, 50, 30)
        hammers_text_rect.topright = (-35, 10)
        hammers_text = gui.elements.UITextBox(
            html_text="",
            relative_rect=hammers_text_rect,
            manager=UI.ui_manager,
            container=hammers,
            object_id="#hammers_text",
            anchors={
                "left": "right",
                "right": "right",
                "top": "top",
                "bottom": "top"
            }
        )
        UI.add(hammers)
        UI.add(hammers_text)

        self.update_text()

    # Пас-ни отрицателно число, за да махнеш
    def add_hammers(self, amount_to_add: int):
        if amount_to_add == 0:
            return
        if amount_to_add < 0:
            if self.amount < -amount_to_add:
                return
        self.amount += amount_to_add
        self.update_text()

    def show(self):
        hammers: gui.elements.UIPanel = UI.get("#hammers")
        hammers.visible = 1

        hammers_text: gui.elements.UIPanel = UI.get("#hammers_text")
        hammers_text.visible = 1

    def update_text(self):
        hammers_text: gui.elements.UITextBox = UI.get("#hammers_text")
        hammers_text.set_text(f'<font face="Pala", color="#111111", size=5>{self.amount}</font>')
