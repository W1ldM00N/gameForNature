import pygame
import sys
from settings import *
from importer import json_dump

font = pygame.font.Font(None, 30)
quiz_font = pygame.font.Font(None, 50)

task = {
    'laborotory': [
        'Покиньте лабороторию'
    ],
    'forest': [
        'Найдите исчезающие виды растений',
        'Опасно! Потушите лесной пожар!'
    ],
    'mountain': [
        'Найдите исчезающие виды растений',
        'Заполните форму по заповеднику'
    ]
}

quiz_len = {
    'mountain': 1,
}

quiz_question = {
    'mountain': [
        'Какой из перечисленных видов растений обитает в этом заповеднике?',
    ]
}

quiz_answers = {
    'mountain': [
        [
            '[1] Яблоня Сиверса',
            '[2] Родиола розовая',
            '[3] Ирис желтый',
            '[4] Ель',
            1
        ],
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
            if self.task_list[self.level][self.task_num] == 'Опасно! Потушите лесной пожар!':
                for sprite in sorted(self.level_class.interactable.sprites(), key=lambda tile: tile.rect.centery):
                    if sprite.type == 'fire invisible':
                        sprite.image = pygame.image.load("../tiles/forest_tiles/fire.png")
                        sprite.type = 'fire visible'
        if self.task_list[self.level][self.task_num] == 'Заполните форму по заповеднику':
            self.quiz_maker(self.level)

    def quiz_maker(self, level):
        for i in range(quiz_len[level]):
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                keys = pygame.key.get_pressed()
                if keys[pygame.K_1]:
                    if quiz_answers[level][i][4] == 1:
                        ans = quiz_font.render('Congrats!', True, 'White')
                    else:
                        ans = quiz_font.render('Wrong!', True, 'White')
                    self.display.blit(ans, (650, 150))
                    pygame.display.update()
                    break
                elif keys[pygame.K_2]:
                    if quiz_answers[level][i][4] == 2:
                        ans = quiz_font.render('Congrats!', True, 'White')
                    else:
                        ans = quiz_font.render('Wrong!', True, 'White')
                    self.display.blit(ans, (650, 150))
                    pygame.display.update()
                    break
                elif keys[pygame.K_3]:
                    if quiz_answers[level][i][4] == 3:
                        ans = quiz_font.render('Congrats!', True, 'White')
                    else:
                        ans = quiz_font.render('Wrong!', True, 'White')
                    self.display.blit(ans, (650, 150))
                    pygame.display.update()
                    break
                elif keys[pygame.K_4]:
                    if quiz_answers[level][i][4] == 4:
                        ans = quiz_font.render('Congrats!', True, 'White')
                    else:
                        ans = quiz_font.render('Wrong!', True, 'White')
                    self.display.blit(ans, (650, 150))
                    pygame.display.update()
                    break

                self.display.fill('black')
                question = quiz_font.render(quiz_question[level][i], True, 'White')
                self.display.blit(question, (15, 30))
                first_ans = quiz_font.render(quiz_answers[level][i][0], True, 'White')
                self.display.blit(first_ans, (30, 200))
                second_ans = quiz_font.render(quiz_answers[level][i][1], True, 'White')
                self.display.blit(second_ans, (30, 300))
                third_ans = quiz_font.render(quiz_answers[level][i][2], True, 'White')
                self.display.blit(third_ans, (530, 200))
                forth_ans = quiz_font.render(quiz_answers[level][i][3], True, 'White')
                self.display.blit(forth_ans, (530, 300))
                pygame.display.update()
        self.complete()
