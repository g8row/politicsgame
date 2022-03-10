from pygame.event import Event
from state import GameState
import pygame
import pygame_gui as gui

from dialogue_box import DialogueBox, DialogueBoxType


def init(gs: GameState):
    gs.ui_manager.add_font_paths("Pala", regular_path="data/fonts/pala.ttf", bold_path="data/fonts/palab.ttf")
    gs.ui_manager.preload_fonts([{"name": "Pala", "point_size": 14, "style": "regular"}, {"name": "Pala", "point_size": 14, "style": "bold"}])

    gs.dialogue_box = DialogueBox(gs.ui_manager)
    gs.dialogue_box.prompt(
        type=DialogueBoxType.JUST_OK,
        title="Здравей",
        desc_html=
        "<font face='Pala', color='#000000', size=4>Добре дошъл.<br><br>Ти си министър-председателят на <b>Република България</b>.<br>От твоя кабинет ще се взимат най-важните решения, от които ще зависи бъдещето на страната.<br><br>Но първо... представи се!</font>"
    )

    gs.dialogue_box.prompt(type=DialogueBoxType.ASK_FOR_IDENTITY, title="Ти си...", desc_html="")


def on_event(gs: GameState, e: Event):
    gs.dialogue_box.on_event(e)


def frame(gs: GameState):
    gs.dialogue_box.frame()
