import pygame

def init(gs):
    gs.room = pygame.image.load("data/room.png")
    gs.desk = pygame.image.load("data/desk.png")
    gs.cherga = pygame.image.load("data/cherga.png")
    gs.flag = pygame.image.load("data/flag.png")
    
def draw(gs):
    gs.win.blit(gs.room, (50, 50))
    gs.win.blit(gs.desk, (50, 50))
    gs.win.blit(gs.cherga, (50, 50))
    gs.win.blit(gs.flag, (50, 50))
    
