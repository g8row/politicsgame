import math

import state.game_state as GS
import state.ui_state as UI

from pygame.event import Event
import pygame
import pygame_gui as gui


class GeneralPrompt:
    #
    # Място за константи, които могат да се използват да се
    # разполагат UI елементите.
    #
    # Oпределят от изображението (GeneralPrompt.png за GeneralDialogueBox)
    #
    # Могат да се access-ват и от child class-ове.
    #
    DIM = 600, 499     # Целия размер на .png

    # Чистото място от прозореца
    USABLE_TOP_LEFT = (28, 43)
    USABLE_DIM = (545, 420)

    PADDING = 25     # Колко пиксела да има между ръбовете на prompt-а и нещата вътре
    ELEMENT_PADDING = 10     # ... същото, но между елементите вътре
    TOP_PADDING_BONUS = 20     # Отгоре има заглавие, което иначе много се бута ако не преместим нещата по-надолу

    # Синьото място горе за заглавие
    TITLE_TOP_LEFT = (200, 13)
    TITLE_DIM = (200, 54)

    # Колко да са големи самите UI елементи, хубаво е да са еднакви във всеки прозорец, за да има consistency
    BUTTON_DIM = (90, 50)
    TEXT_ENTRY_DIM = (130, 25)

    # Самото геройче дето излиза в началото на играта, когато те пита за името
    CHARACTER_DIM = (80, 110)

    manager: gui.UIManager

    panel: gui.elements.UIPanel
    title: gui.elements.UILabel

    # Неща за анимация...
    target_alpha_t: float = 0
    alpha_t: float = 0
    alpha: int = 255
    animation_duration: float = 0.3

    anim_render_target: pygame.surface.Surface
    anim_render_target_alpha: pygame.surface.Surface

    anim_width: int
    anim_height: int

    def __init__(self):
        self.anim_width, self.anim_height = GS.win_size

        self.manager = UI.pool_get_ui_manager()
        self.anim_render_target = UI.pool_get_window_surface()
        self.anim_render_target_alpha = UI.pool_get_alpha_window_surface()

        self.panel = gui.elements.UIPanel(
            relative_rect=center(self.manager.root_container, self.DIM),
            starting_layer_height=10,
            manager=self.manager,
            object_id="#dialogue_box",
            visible=0
        )

        self.title = gui.elements.UILabel(
            relative_rect=pygame.Rect((0, 0), (-1, -1)),
            text="Ти си...",
            manager=self.manager,
            container=self.panel,
            object_id="#dialogue_box_title",
            visible=0
        )

    def __del__(self):
        self.panel.kill()     # Също убива и децата му на панела
        UI.pool_return_ui_manager(self.manager)
        UI.pool_return_window_surface(self.anim_render_target)
        UI.pool_return_alpha_window_surface(self.anim_render_target_alpha)

    def set_title(self, title: str):
        self.title.set_text(title)

        # Центрирай заглавието
        x, y = self.TITLE_TOP_LEFT
        w, h = self.TITLE_DIM
        x += w / 2
        y += h / 2
        x -= self.title.rect.width / 2
        y -= self.title.rect.height / 2
        self.title.set_relative_position((x, y))

    # Това се вика от state.ui_state, защото там е логиката за queue-ването!
    def show(self, animation: bool):
        self.panel.show()
        if animation:
            self.panel.disable()
            self.target_alpha_t = 1.0
        else:
            # Скипни анимацията.. (ако прозорчетата са били в queue)
            self.panel.enable()
            self.alpha_t = self.target_alpha_t = 1.0
            self.alpha = 255

    # Това се вика от state.ui_state, защото там е логиката за queue-ването!
    def hide(self, animation: bool):
        if animation:
            self.panel.disable()
            self.target_alpha_t = 0.0
            UI.set_prompt_in_hide(self)
        else:
            # Скипни анимацията.. (ако прозорчетата са били в queue)
            self.panel.hide()

    def frame(self):
        self.manager.update(GS.dt)

        if self.target_alpha_t != self.alpha_t:
            if abs(self.target_alpha_t - self.alpha_t) < 0.001:
                self.alpha_t = self.target_alpha_t
                if self.target_alpha_t == 1.0:
                    self.panel.enable()
                if self.target_alpha_t == 0.0:
                    UI.prompt_done_hiding(self)
            else:
                if self.target_alpha_t == 1.0:
                    self.alpha_t += 1 / self.animation_duration * (1 / 60)
                else:
                    self.alpha_t -= 1 / self.animation_duration * (1 / 60)

            self.alpha = int(slerp(0.0, 1.0, self.alpha_t) * 255.0)

            w, h = GS.win_size
            self.anim_width = int(slerp(0.8 * w, w, self.alpha_t))
            self.anim_height = int(slerp(0.8 * h, h, self.alpha_t))

            # Цялата тази простотия ни струва 10 FPS, но май няма по-бърз начин
            # защото работим с прозрачни изображения и библиотеката няма по-хубав API и това е тъжно.
            self.anim_render_target_alpha.fill((0, 0, 0, 0))
            self.manager.draw_ui(self.anim_render_target_alpha)

            #self.ui_render_target_alpha.fill("0xfff6d9")
            self.anim_render_target.blit(GS.win, (0, 0))
            self.anim_render_target.blit(self.anim_render_target_alpha, (0, 0))
            self.anim_render_target.set_alpha(self.alpha)

            scaled = pygame.transform.scale(self.anim_render_target, (self.anim_width, self.anim_height))
            GS.win.blit(scaled, ((w - self.anim_width) // 2, (h - self.anim_height) // 2))
        else:
            self.manager.draw_ui(GS.win)

    def on_event(self, e: Event):
        self.manager.process_events(e)


def center(container: gui.core.UIContainer, size: tuple[int | float, int | float]):
    x, y = container.rect.center
    w, h = size
    x -= w / 2
    y -= h / 2
    return pygame.Rect((x, y), (w, h))


def slerp(x: float, x1: float, t: float) -> float:
    rad = math.pi / 4     # math.acos(x * x1)     # + y*y1 )
    newX = x * math.sin((1.0 - t) * rad) / math.sin(rad)
    newX += x1 * math.sin(t * rad) / math.sin(rad)
    return newX


def get_alpha_image(original_image: pygame.Surface, alpha: int):
    image = original_image.copy()
    tmp = pygame.Surface(image.get_rect().size)
    tmp.blit(image.convert(), (0, 0))
    tmp.set_alpha(alpha)
    tmp.set_colorkey((0, 0, 0))
    image.blit(tmp, (0, 0))
    return image
