import state.game_state as GS
import state.ui_state as UI

from pygame.event import Event
import pygame
import pygame_gui as gui

from prompts.prompt_just_ok import PromptJustOk
from prompts.prompt_ask_for_identity import PromptAskForIdentity


def init():
    pass


def on_event(e: Event):
    if UI.active_prompt is not None:
        UI.active_prompt.on_event(e)

    if e.type == pygame.KEYDOWN and e.key == pygame.K_F3:
        UI.prompt(PromptJustOk(title="Здравей", desc_html="Баница"))


def frame():
    if UI.active_prompt is not None:
        UI.active_prompt.frame()
    if UI.prompt_in_hide is not None:
        UI.prompt_in_hide.frame()
