import pygame
from player import Player
from importer import import_csv, import_tiles, import_json
from interactions import InteractGroup
from builder import *
from tasks import Task

font = pygame.font.Font(None, 30)


class Level:
    def __init__(self):
        self.display = pygame.display.get_surface()

        self.level = 'laborotory'

        self.visible = CameraGroup()
        self.background = CameraGroup(level=self.level)
        self.obstacles = pygame.sprite.Group()
        self.interactable = InteractGroup()
        self.tasks = Task(self)
        self.player = None
        self.save = import_json(SAVE_PATH)

        self.create_map()

    def create_map(self):
        self.visible.empty()
        self.background.empty()
        self.obstacles.empty()
        self.interactable.empty()
        self.background.remake(self.level)

        csvs = {
            'laborotory': {
                'furniture': import_csv('../maps/lab/lab_map_furniture.csv'),
                'lab': import_csv('../maps/lab/lab_map.csv'),
                'interactions': import_csv('../maps/lab/lab_interactions.csv')
            },
            'forest': {
                'water': import_csv('../maps/forest/forest_map_water.csv'),
                'fire': import_csv('../maps/forest/forest_map_fire.csv'),
                'tree': import_csv('../maps/forest/forest_map_trees.csv'),
                'pine_tree': import_csv('../maps/forest/forest_map_pine trees.csv'),
                'red_book_1': import_csv('../maps/forest/forest_map_Trollius asiaticus.csv'),
                'red_book_2': import_csv('../maps/forest/forest_map_Rhodiola rosea.csv')
            },
            'mountain': {
                'apple_tree': import_csv('../maps/mountain/mountain_map_apple_tree.csv'),
                'borders': import_csv('../maps/mountain/mountain_map_borders.csv'),
                'tree': import_csv('../maps/mountain/mountain_map_tree.csv'),
                'pine_tree': import_csv('../maps/mountain/mountain_map_pine_tree.csv'),
                'red_book': import_csv('../maps/mountain/mountain_map_red book.csv'),
            },
            'sea': {
                'asdf': import_csv('../maps/sea/sea_asdf.csv'),
                'qwert6': import_csv('../maps/sea/sea_qwert6.csv'),
                'borders': import_csv('../maps/sea/sea_borders.csv')
            }
        }
        tiles = {
            'laborotory': import_tiles("../tiles/lab_tiles"),
            'forest': import_tiles('../tiles/forest_tiles')
        }

        if self.level == 'laborotory' and not IS_TASKED:
            lab_builder(csvs, tiles, self.obstacles, self.visible, self.background, self.interactable)
            self.player = Player((280, 328), self.visible, self.obstacles)
        elif self.save['last_level'] == 1 and not IS_TASKED:
            forest_builder(csvs, tiles, self.obstacles, self.visible, self.interactable)
            self.player = Player((280, 750), self.visible, self.obstacles)
        elif self.save['last_level'] == 2 and not IS_TASKED:
            mountain_builder(csvs, self.obstacles, self.interactable)
            self.player = Player((1750, 1500), self.visible, self.obstacles)
        elif self.save['last_level'] == 3 and not IS_TASKED:
            sea_builder(csvs, self.obstacles, self.interactable)
            self.player = Player((1750, 1750), self.visible, self.obstacles)

    def run(self):
        self.background.running_draw(self.player)
        self.visible.running_draw(self.player)
        self.visible.update()
        self.interactable.running_draw(self.player)
        self.interactable.possible_interactions(self.player, self)
        self.tasks.update()
        self.tasks.display_task()


class CameraGroup(pygame.sprite.Group):
    def __init__(self, level=None):
        super().__init__()
        self.display = pygame.display.get_surface()
        self.half_width = self.display.get_width() // 2
        self.half_height = self.display.get_height() // 2
        self.offset = pygame.math.Vector2()

        self.level = level

        if level == 'forest':
            self.floor_surf = pygame.image.load('../tiles/forest_tiles/background.png').convert()
            self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))
        if level == 'mountain':
            self.floor_surf = pygame.image.load('../tiles/mountain_tiles/mountain_map.png').convert()
            self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def running_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        if self.level is not None and self.level != 'laborotory':
            background_pos = self.floor_rect.topleft - self.offset
            self.display.blit(self.floor_surf, background_pos)

        for sprite in sorted(self.sprites(), key=lambda tile: tile.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display.blit(sprite.image, offset_pos)

    def remake(self, level):
        self.level = level

        if level == 'forest':
            self.floor_surf = pygame.image.load('../tiles/forest_tiles/background.png').convert()
            self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))
        elif level == 'mountain':
            self.floor_surf = pygame.image.load('../tiles/mountain_tiles/mountain_map.png').convert()
            self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))
        elif level == 'sea':
            self.floor_surf = pygame.image.load('../tiles/sea_tiles/sea.png').convert()
            self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))
