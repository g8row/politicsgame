import state.game_state as GS
import state.ui_state as UI

from pygame.event import Event
import pygame
import pygame_gui as gui

from prompts.prompt_just_ok import PromptJustOk
from prompts.prompt_ask_for_identity import PromptAskForIdentity


def init():
    UI.non_animated_ui_manager = UI.pool_get_ui_manager()
    UI.non_animated_ui_manager.preload_fonts([{"name": "Pala", "point_size": 16, "style": "regular"}])

    calendar_rect = pygame.Rect(0, 0, 141, 51)
    calendar_rect.topright = (-20, 20)

    calendar = gui.elements.UIPanel(
        relative_rect=calendar_rect,
        starting_layer_height=1,
        manager=UI.non_animated_ui_manager,
        object_id="#calendar",
        anchors={
            "left": "right",
            "right": "right",
            "top": "top",
            "bottom": "top"
        },
        container=UI.non_animated_ui_manager.root_container
    )

    calendar_text_rect = pygame.Rect(10, 11, 121, 31)
    calendar_text = gui.elements.UITextBox(
        html_text='<font face="Pala", color="#111111", size=4.5>2020-01-01</font>',
        relative_rect=calendar_text_rect,
        manager=UI.non_animated_ui_manager,
        container=calendar,
        object_id="#calendar_text"
    )

    UI.add(calendar)
    UI.add(calendar_text)


def on_event(e: Event):
    UI.non_animated_ui_manager.process_events(e)

    if UI.active_prompt is not None:
        UI.active_prompt.on_event(e)

    if e.type == pygame.KEYDOWN and e.key == pygame.K_F3:
        UI.prompt(PromptJustOk(title="Здравей", desc_html="Баница"))


def frame():
    UI.non_animated_ui_manager.update(GS.dt)
    UI.non_animated_ui_manager.draw_ui(GS.non_animated_ui_surface)

    if UI.active_prompt is not None:
        UI.active_prompt.frame()
    if UI.prompt_in_hide is not None:
        UI.prompt_in_hide.frame()
