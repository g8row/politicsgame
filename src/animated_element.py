import math

import state.game_state as GS
import state.ui_state as UI

from pygame.event import Event
import pygame
import pygame_gui as gui

from overrides import EnforceOverrides


class AnimatedElement(EnforceOverrides):
    animation_duration: float = 0.2

    t: float = 0
    target_t: float = 0

    alpha: int = 255

    def __init__(self):
        pass

    def begin_alpha_animation(self, target_visible: bool):
        self.target_t = 1.0 if target_visible else 0.0

    def skip_alpha_animation(self, visible: bool):
        if visible:
            self.t = self.target_t = 1.0
            self.alpha = 255
        else:
            self.t = self.target_t = 0.0
            self.alpha = 0

    def on_t_reached_1(self):
        pass

    def on_t_reached_0(self):
        pass

    def on_t_changed(self, alpha: int, t: float):
        pass

    def frame(self):
        if self.target_t != self.t:
            if abs(self.target_t - self.t) < 0.001:
                self.t = self.target_t
                if self.target_t == 1.0:
                    self.on_t_reached_1()
                if self.target_t == 0.0:
                    self.on_t_reached_0()
            else:
                if self.target_t == 1.0:
                    self.t += 1 / self.animation_duration * (1 / 60)
                else:
                    self.t -= 1 / self.animation_duration * (1 / 60)

            self.alpha = int(slerp(0.0, 1.0, self.t) * 255.0)
            self.on_t_changed(self.alpha, self.t)


def slerp(x: float, x1: float, t: float) -> float:
    rad = math.pi / 4     # math.acos(x * x1)     # + y*y1 )
    newX = x * math.sin((1.0 - t) * rad) / math.sin(rad)
    newX += x1 * math.sin(t * rad) / math.sin(rad)
    return newX
