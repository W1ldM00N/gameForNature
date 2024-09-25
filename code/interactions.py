import pygame
from settings import *
from importer import import_json

pygame.init()
font = pygame.font.Font(None, 30)

distance = {
    'interactable10': 1.5,
    'Rhodiola rosea': 1.5,
    'Trollius asiaticus': 1.5,
    'fire': 0,
}

taskStuffInteracted = {
    "interactable10": False,
    "fire": False,
    "Trollius asiaticus": False,
    "Rhodiola rosea": False,
}


class InteractGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display = pygame.display.get_surface()

    def possible_interactions(self, player, level):
        save = import_json(SAVE_PATH)
        for sprite in self.sprites():
            if abs(sprite.rect.centery - player.rect.centery) <= distance[sprite.type] * TILESIZE and \
                    abs(sprite.rect.centerx - player.rect.centerx) <= distance[sprite.type] * TILESIZE and \
                    not taskStuffInteracted[sprite.type]:

                # interaction message
                interact = font.render('press x to interact', True, 'White')
                interact_rect = self.display.get_rect(topleft=(580, 680))
                self.display.blit(interact, interact_rect)

                # check for keyboard_input
                keys = pygame.key.get_pressed()

                if keys[pygame.K_x]:
                    if sprite.type == 'interactable10':
                        level.level = LEVEL_NAME[save["last_level"]]
                        level.create_map()
                    elif sprite.type == "Trollius asiaticus" or \
                            sprite.type == "Rhodiola rosea":
                        if not taskStuffInteracted[sprite.type]:
                            taskStuffInteracted[sprite.type] = True
                        if taskStuffInteracted["Trollius asiaticus"] and \
                                taskStuffInteracted["Rhodiola rosea"]:
                            level.tasks.complete()
