from pygame.event import Event
import state.ui_state as UI

import pygame
import pygame_gui as gui


class Calendar():
    def __init__(self):
        calendar_rect = pygame.Rect(0, 0, 141, 51)
        calendar_rect.topright = (-20, 20)

        calendar = gui.elements.UIPanel(
            relative_rect=calendar_rect,
            starting_layer_height=1,
            manager=UI.ui_manager,
            object_id="#calendar",
            anchors={
                "left": "right",
                "right": "right",
                "top": "top",
                "bottom": "top"
            }
        )

        calendar_text_rect = pygame.Rect(10, 11, 121, 31)
        calendar_text = gui.elements.UITextBox(
            html_text='<font face="Pala", color="#111111", size=4.5>2020-01-01</font>',
            relative_rect=calendar_text_rect,
            manager=UI.ui_manager,
            container=calendar,
            object_id="#calendar_text"
        )

        UI.add(calendar)
        UI.add(calendar_text)