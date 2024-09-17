import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, img_type, surface=pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)

        self.type = img_type
        self.image = surface

        # if self.type == 'object':
        #     self.rect = self.img.get_rect(topleft=(pos[0], pos[1]-TILESIZE))
        # else:
        #     self.rect = self.img.get_rect(topleft=pos)
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -5)
