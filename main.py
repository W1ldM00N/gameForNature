import pygame
import sys

# initialization
pygame.init()

# display creation
screen = pygame.display.set_mode((1000, 750))
pygame.display.set_caption('Nature')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
