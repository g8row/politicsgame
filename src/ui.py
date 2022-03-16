import state.game_state as GS
import state.ui_state as UI

from pygame.event import Event
import pygame
import pygame_gui as gui

from prompts.prompt_just_ok import PromptJustOk
from prompts.prompt_ask_for_identity import PromptAskForIdentity


def init():
    # Тук слагаме неща при зареждане, така че да не забива по-късно,
    # когато за пръв път се използва. За font-ове pygame_gui предупреждава
    # и принтира в конзолата точно какво да се сложи тук.

    UI.prompt(
        PromptJustOk(
            title="Здравей",
            desc_html=
            "<font face='Pala', color='#000000', size=4>Добре дошъл.<br><br>Ти си министър-председателят на <b>Република България</b>.<br>От твоя кабинет ще се взимат най-важните решения, от които ще зависи бъдещето на страната.<br><br>Но първо... представи се!</font>"
        )
    )

    # Веднага едно след друго питай за име и т.н.,
    # нещата се queue-ват, второто се показва след като цъкне "Добре" на първото.
    UI.prompt(PromptAskForIdentity())


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
