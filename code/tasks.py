import pygame
import sys
from settings import *
from importer import json_dump

font = pygame.font.Font(None, 30)

task = {
    'laborotory': [
        'Leave the lab'
    ],
    'forest': [
        'Find endangered plants',
        'Warning! Stop the fire!'
    ],
    'mountain': [
        'Find endangered plants',
    ]
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
        if self.level != self.level_class.level:
            self.level = self.level_class.level
            self.task_num = 0

    def complete(self):
        self.task_num += 1
        if self.task_num == len(self.task_list[self.level]):
            if self.level == 'laborotory':
                self.level_class.level = self.level_class.save['last_level']
                self.level_class.create_map()
                return
            y = 0
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    break
                if keys[pygame.K_UP] and y < 0:
                    y += 5
                elif keys[pygame.K_DOWN] and y > -1810*LEVEL_SUM[self.level]+810:
                    y -= 5

                self.display.fill('black')
                for i in range(0, LEVEL_SUM[self.level]):
                    image = pygame.image.load("../tiles/level_sum/" + self.level + "_" + str(i+1) + ".jpg")
                    self.display.blit(image, (0, y+i*1810))
                pygame.display.update()

            self.level_class.save['last_level'] += 1
            json_dump(SAVE_PATH, self.level_class.save)
            self.level_class.level = LEVEL_NAME[0]
            self.level = self.level_class.level
            self.task_num = 0
            self.level_class.create_map()
        if self.level == 'forest':
            if self.task_list[self.level][self.task_num] == 'Warning! Stop the fire!':
                for sprite in sorted(self.level_class.interactable.sprites(), key=lambda tile: tile.rect.centery):
                    if sprite.type == 'fire invisible':
                        sprite.image = pygame.image.load("../tiles/forest_tiles/fire.png")
                        sprite.type = 'fire visible'
