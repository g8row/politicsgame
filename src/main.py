import sys
import time
import pygame
pygame.init()

def frame(gs):
    # Тук се случва цялата логика за всеки фрейм
    
    room.draw(gs)

win = pygame.display.set_mode((500, 500), pygame.DOUBLEBUF)  # Прозорец
pygame.display.set_caption("republika lol")                  # Заглавие

   
# Game state, всички могат да слагат (и махат) неща в тази променилива
from types import SimpleNamespace
gs = SimpleNamespace()            
gs.win = win            # пример..., някои функции искат да имат прозореца 


import room
room.init(gs)

target_fps = 60                               
frame_time_ns = 1.0 / target_fps * 10 ** 9     # Колко наносекунди трябва да продължава всеки фрейм (логика + рисуване), за да hit-нем target FPS-а

prev_time = time.time_ns()                      
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()
    
    frame(gs)
    
    pygame.display.flip()
    
    # Локва играта да рънва на 60 FPS вместо да точи процесора:
    curr_time = time.time_ns()
    diff = curr_time - prev_time
    prev_time = curr_time

    time.sleep(max(frame_time_ns - diff, 0) / 10 ** 9)

