import pygame
import settings
from importer import import_json
import sys

pygame.init()
font = pygame.font.Font(None, 30)

distance = {
    'interactable10': 1.5,
    'Rhodiola rosea': 1.5,
    'Trollius asiaticus': 1.5,
    'fire visible': 3,
    'fire invisible': 0,
    'water': 1,
    'apple': 1.5,
    'flower': 1.5
}

taskStuffInteracted = {
    "interactable10": False,
    "fire visible": False,
    "fire invisible": True,
    "Trollius asiaticus": False,
    "Rhodiola rosea": False,
    "water": False,
    'apple': False,
    'flower': False
}

fireCount = 5 - 4


class InteractGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display = pygame.display.get_surface()
        self.half_width = self.display.get_width() // 2
        self.half_height = self.display.get_height() // 2
        self.offset = pygame.math.Vector2()

    def possible_interactions(self, player, level):
        save = import_json(settings.SAVE_PATH)
        for sprite in self.sprites():
            if abs(sprite.rect.centery - player.rect.centery) <= distance[sprite.type] * settings.TILESIZE and \
                    abs(sprite.rect.centerx - player.rect.centerx) <= distance[sprite.type] * settings.TILESIZE and \
                    not taskStuffInteracted[sprite.type]:

                # interaction message
                interact = font.render('press x to interact', True, 'White')
                interact_rect = self.display.get_rect(topleft=(580, 680))
                self.display.blit(interact, interact_rect)

                # check for keyboard_input
                keys = pygame.key.get_pressed()

                if keys[pygame.K_x]:
                    if sprite.type == 'interactable10':
                        level.level = settings.LEVEL_NAME[save["last_level"]]
                        level.create_map()
                    elif sprite.type == "Trollius asiaticus" or \
                            sprite.type == "Rhodiola rosea" or \
                            sprite.type == "apple" or \
                            sprite.type == "flower":
                        if not taskStuffInteracted[sprite.type]:
                            taskStuffInteracted[sprite.type] = True

                        y = 0
                        while True:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    settings.IS_TASKED = False
                                    pygame.quit()
                                    sys.exit()

                            keys = pygame.key.get_pressed()
                            if keys[pygame.K_ESCAPE]:
                                settings.IS_TASKED = False
                                break
                            if keys[pygame.K_UP] and y < 0:
                                y += 5
                            elif keys[pygame.K_DOWN] and y > -1000:
                                y -= 5

                            settings.IS_TASKED = True
                            self.display.fill('black')
                            image = pygame.image.load("../tiles/endangered_images/" + sprite.type + ".jpg")
                            self.display.blit(image, (0, y))
                            pygame.display.update()

                        if taskStuffInteracted["Trollius asiaticus"] and \
                                taskStuffInteracted["Rhodiola rosea"]:
                            level.tasks.complete()
                        if taskStuffInteracted["apple"] and \
                                taskStuffInteracted["flower"]:
                            level.tasks.complete()

                    elif sprite.type == "water":
                        player.hasWater = True
                        interact = font.render('You took water', True, 'White')
                        interact_rect = self.display.get_rect(topleft=(595, 640))
                        self.display.blit(interact, interact_rect)
                    elif sprite.type == "fire visible":
                        if not player.hasWater:
                            interact = font.render('You have no water', True, 'White')
                            interact_rect = self.display.get_rect(topleft=(580, 640))
                            self.display.blit(interact, interact_rect)
                        else:
                            sprite.type = 'fire invisible'
                            player.hasWater = False
                            global fireCount
                            if fireCount - 1 == 0:
                                taskStuffInteracted['fire visible'] = False
                                level.tasks.complete()
                            else:
                                fireCount -= 1

    def running_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for sprite in sorted(self.sprites(), key=lambda tile: tile.rect.centery):
            try:
                if sprite.type.split(" ")[1] == "visible":
                    offset_pos = sprite.rect.topleft - self.offset
                    self.display.blit(sprite.image, offset_pos)
            except IndexError:
                continue
