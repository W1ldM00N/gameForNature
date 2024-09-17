import pygame
from settings import *
from tile import Tile
from player import Player
from importer import import_csv, import_tiles


class Level:
    def __init__(self):
        self.display = pygame.display.get_surface()

        self.visible = CameraGroup()
        self.background = CameraGroup()
        self.obstacles = pygame.sprite.Group()
        self.player = None

        self.create_map()

    def create_map(self):
        csvs = {
            'laborotory': {
                # 'obstacles': import_csv('../maps/lab/lab_map_obstacles.csv'),
                'furniture': import_csv('../maps/lab/lab_map_furniture.csv'),
                # 'go_button': import_csv('../maps/lab/lab_map_go.csv'),
                # 'player_location': import_csv('../maps/lab/lab_map_player.csv'),
                # 'lab_stuff': import_csv('../maps/lab/lab_map_stuff.csv'),
                'lab': import_csv('../maps/lab/lab_map.csv')
            },
        }
        tiles = {
            'laborotory': import_tiles("../tiles/lab_tiles")
        }

        for csv_type, csv_item in csvs['laborotory'].items():
            for row_i, row in enumerate(csv_item):
                for col_i, col in enumerate(row):
                    if col != '-1':
                        x = col_i * TILESIZE
                        y = row_i * TILESIZE
                        # if csv_type == 'obstacles':
                        #     Tile((x, y), [self.obstacles], 'obstacle')
                        if csv_type == 'furniture':
                            try:
                                # print(tiles['laborotory'])
                                image = tiles['laborotory'][col + '.png']
                                Tile((x, y), (self.obstacles, self.visible), 'object', image)
                            except KeyError:
                                # print(col + '.png')
                                continue
                        if csv_type == 'lab':
                            try:
                                image = tiles['laborotory'][col + '.png']
                                if col == '118' or col == '119' or col == '120' or col == '129' or col == '130' or col == '131':
                                    Tile((x, y), (self.background,), 'object', image)
                                else:
                                    Tile((x, y), (self.obstacles, self.background,), 'object', image)
                            except KeyError:
                                continue
        self.player = Player((280, 328), self.visible, self.obstacles)

    def run(self):
        self.background.running_draw(self.player)
        self.visible.running_draw(self.player)
        self.visible.update()


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display = pygame.display.get_surface()
        self.half_width = self.display.get_width() // 2
        self.half_height = self.display.get_height() // 2
        self.offset = pygame.math.Vector2()

    def running_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display.blit(sprite.image, offset_pos)

        # for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
        #     offset_pos = sprite.rect.topleft - self.offset
        #     sprite.rect.topleft = offset_pos