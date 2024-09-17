import pygame
from settings import *

pygame.init()
font = pygame.font.Font(None, 30)


class InteractGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display = pygame.display.get_surface()

    def possible_interactions(self, player, level):
        for sprite in self.sprites():
            if abs(sprite.rect.centery - player.rect.centery) <= 1.5*TILESIZE and \
                    abs(sprite.rect.centerx - player.rect.centerx) <= 1.5*TILESIZE:

                # interaction message
                interact = font.render('press x to interact', True, 'White')
                interact_rect = self.display.get_rect(topleft=(580, 680))
                pygame.draw.rect(self.display, 'Black', interact_rect)
                self.display.blit(interact, interact_rect)

                # check for keyboard_input
                keys = pygame.key.get_pressed()

                if keys[pygame.K_x]:
                    if sprite.type == 'interactable10':
                        level.level = LEVEL_NAME[LEVEL]
                        level.create_map()
                        print('10//')
