import pygame
from settings import *

font = pygame.font.Font(None, 30)

task = {
    'laborotory': [
        'leave the lab'
    ],
    'forest': [
        'take a photos of endangered plants'
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
        self.level = LEVEL_NAME[self.level_class.save["level"]]
        self.task_num = 0

    def complete(self):
        self.task_num += 1
        if self.task_num == len(self.task_list[self.level]):
            self.level_class.level = LEVEL_NAME[self.level_class.save["last_level"] + 1]
            self.level_class.create_map()
