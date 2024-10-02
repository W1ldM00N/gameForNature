import pygame
from settings import *

font = pygame.font.Font(None, 30)

task = {
    'laborotory': [
        'Leave the lab'
    ],
    'forest': [
        'Find endangered plants',
        'Warning! Stop the fire!'
    ],
}


class Task:
    def __init__(self, level):
        self.display = pygame.display.get_surface()
        self.level = 'laborotory'
        self.task_num = 0
        self.task_list = task
        self.level_class = level

    def display_task(self):
        rendered_task = font.render(self.task_list[self.level][self.task_num], True, 'White')
        self.display.blit(rendered_task, (15, 15))

    def update(self):
        if self.level != LEVEL_NAME[self.level_class.save["level"]]:
            self.level = LEVEL_NAME[self.level_class.save["level"]]
            self.task_num = 0

    def complete(self):
        self.task_num += 1
        if self.task_num == len(self.task_list[self.level]):
            self.level_class.level = LEVEL_NAME[self.level_class.save["last_level"] + 1]
            self.level_class.create_map()
        if self.task_list[self.level][self.task_num] == 'Warning! Stop the fire!':
            for sprite in sorted(self.level_class.interactable.sprites(), key=lambda tile: tile.rect.centery):
                if sprite.type == 'fire invisible':
                    sprite.image = pygame.image.load("../tiles/forest_tiles/fire.png")
                    sprite.type = 'fire visible'
