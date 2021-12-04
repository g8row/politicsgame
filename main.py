import pygame
from sys import exit

print('hello pygame')


width, height =  800, 600

pygame.init();
screen = pygame.display.set_mode((width,height))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()
