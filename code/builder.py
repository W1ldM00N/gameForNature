from settings import *
from tile import Tile


def lab_builder(csvs, tiles, obstacles, visible, background, interactable):
    for csv_type, csv_item in csvs['laborotory'].items():
        for row_i, row in enumerate(csv_item):
            for col_i, col in enumerate(row):
                if col != '-1':
                    x = col_i * TILESIZE
                    y = row_i * TILESIZE
                    if csv_type == 'furniture':
                        try:
                            image = tiles['laborotory'][col + '.png']
                            Tile((x, y), (obstacles, visible), 'object', image)
                        except KeyError:
                            continue
                    if csv_type == 'lab':
                        try:
                            image = tiles['laborotory'][col + '.png']
                            if col == '118' or col == '119' or col == '120' or \
                                    col == '129' or col == '130' or col == '131':
                                Tile((x, y), background, 'object', image)
                            else:
                                Tile((x, y), (obstacles, background,), 'object', image)
                        except KeyError:
                            continue
                    if csv_type == 'interactions':
                        Tile((x, y), interactable, 'interactable' + col)


def forest_builder(csvs, tiles, obstacles, visible, interactable):
    for csv_type, csv_item in csvs['forest'].items():
        for row_i, row in enumerate(csv_item):
            for col_i, col in enumerate(row):
                if col != '-1':
                    x = col_i * TILESIZE
                    y = row_i * TILESIZE
                    if csv_type == 'pine_tree':
                        try:
                            image = tiles['forest']['pineTree' + col + '.png']
                            Tile((x, y), (visible, obstacles), 'object', image)
                        except KeyError:
                            continue
                    if csv_type == 'water':
                        try:
                            image = tiles['forest'][col + '.png']
                            Tile((x, y), (visible, obstacles), 'object', image)
                        except KeyError:
                            continue
                    if csv_type == 'interactions':
                        Tile((x, y), interactable, 'interactable' + col)

                    if csv_type == 'fire':
                        Tile((x, y), interactable, 'fire')