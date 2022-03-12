import math

import state.game_state as GS
import state.ui_state as UI

from pygame.event import Event
import pygame
import pygame_gui as gui


class AnimatedElement:
    manager: gui.UIManager

    target_alpha_t: float = 0
    alpha_t: float = 0
    alpha: int = 255
    animation_duration: float = 0.3

    anim_render_target: pygame.surface.Surface
    anim_render_target_alpha: pygame.surface.Surface

    anim_width: int
    anim_height: int

    container: gui.elements.UIPanel

    def __init__(self):
        self.anim_width, self.anim_height = GS.win_size

        self.manager = UI.pool_get_ui_manager()
        self.anim_render_target = UI.pool_get_window_surface()
        self.anim_render_target_alpha = UI.pool_get_alpha_window_surface()

    def __del__(self):
        self.container.kill()     # Също убива и децата му
        UI.pool_return_ui_manager(self.manager)
        UI.pool_return_window_surface(self.anim_render_target)
        UI.pool_return_alpha_window_surface(self.anim_render_target_alpha)

    # Това се вика от state.ui_state, защото там е логиката за queue-ването!
    def show(self, animation: bool):
        self.container.show()
        if animation:
            self.container.disable()
            self.target_alpha_t = 1.0
        else:
            # Скипни анимацията.. (ако прозорчетата са били в queue)
            self.container.enable()
            self.alpha_t = self.target_alpha_t = 1.0
            self.alpha = 255

    # Това се вика от state.ui_state, защото там е логиката за queue-ването!
    def hide(self, animation: bool):
        if animation:
            self.container.disable()
            self.target_alpha_t = 0.0
            UI.set_prompt_in_hide(self)
        else:
            # Скипни анимацията.. (ако прозорчетата са били в queue)
            self.container.hide()

    def frame(self):
        self.manager.update(GS.dt)

        if self.target_alpha_t != self.alpha_t:
            if abs(self.target_alpha_t - self.alpha_t) < 0.001:
                self.alpha_t = self.target_alpha_t
                if self.target_alpha_t == 1.0:
                    self.container.enable()
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


def slerp(x: float, x1: float, t: float) -> float:
    rad = math.pi / 4     # math.acos(x * x1)     # + y*y1 )
    newX = x * math.sin((1.0 - t) * rad) / math.sin(rad)
    newX += x1 * math.sin(t * rad) / math.sin(rad)
    return newX
