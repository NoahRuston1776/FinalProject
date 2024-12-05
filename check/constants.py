import pygame

pygame.display.init()
info = pygame.display.Info()
height, width = info.current_h, info.current_w
WIDTH, HEIGHT = width, height
#WIDTH, HEIGHT = 1300, 1300
ROWS, COLS = 8, 8
SQUARE_SIZE = HEIGHT//ROWS
FPS = 60

 # RGB colors

RED = (255, 0, 0)   #pure red is (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)

CROWN = pygame.transform.scale(pygame.image.load('check/assets/crown.png'), (45, 25))
