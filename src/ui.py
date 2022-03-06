from pygame.event import Event
from state import GameState
import pygame
import pygame_gui as gui

from dialogue_box import DialogueBox


def init(gs: GameState):
    gs.ui_manager.add_font_paths("Pala", regular_path="data/fonts/pala.ttf", bold_path="data/fonts/palab.ttf")
    gs.ui_manager.preload_fonts([{"name": "Pala", "point_size": 13, "style": "regular"}, {"name": "Pala", "point_size": 13, "style": "bold"}])

    gs.dialogue_box = DialogueBox(gs.ui_manager)
    gs.dialogue_box.set_title("Опа, здравей")
    gs.dialogue_box.set_desc(
        "<font face='Pala', color='#000000', size=4>Добре дошъл.<br><br>Ти си министър-председателят на <b>Република България</b>.<br>От твоя кабинет ще се взимат най-важните решения, от които ще зависи бъдещето на страната.<br><br>Но първо... представи се.</font>"
    )


def on_event(gs: GameState, e: Event):
    if e.type == pygame.MOUSEBUTTONDOWN and e.button == pygame.BUTTON_LEFT:
        mx, my = pygame.mouse.get_pos()
        desc = gs.dialogue_box.desc
        if desc.rect.collidepoint((mx, my)):
            if desc.active_text_effect is not None:
                desc.active_text_effect.time_per_letter = 0.00001


def frame(gs: GameState):
    pass
