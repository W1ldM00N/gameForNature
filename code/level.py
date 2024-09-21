import pygame
from player import Player
from importer import import_csv, import_tiles
from interactions import InteractGroup
from builder import *

font = pygame.font.Font(None, 30)


class Level:
    def __init__(self):
        self.display = pygame.display.get_surface()

        self.level = 'laborotory'

        self.visible = CameraGroup()
        self.background = CameraGroup(level=self.level)
        self.obstacles = pygame.sprite.Group()
        self.interactable = InteractGroup()
        self.player = None

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
                'interactions': import_csv('../maps/forest/forest_map_intaeractable.csv'),
                'trees': import_csv('../maps/forest/forest_map_trees.csv'),
                'pine_tree': import_csv('../maps/forest/forest_map_pine trees.csv')
            },
        }
        tiles = {
            'laborotory': import_tiles("../tiles/lab_tiles"),
            'forest': import_tiles('../tiles/forest_tiles')
        }

        if self.level == 'laborotory':
            lab_builder(csvs, tiles, self.obstacles, self.visible, self.background, self.interactable)
            self.player = Player((280, 328), self.visible, self.obstacles)
        elif self.level == 'forest':
            forest_builder(csvs, tiles, self.obstacles, self.visible, self.interactable)
            self.player = Player((280, 750), self.visible, self.obstacles)

    def run(self):
        self.background.running_draw(self.player)
        self.visible.running_draw(self.player)
        self.visible.update()
        self.interactable.possible_interactions(self.player, self)


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
