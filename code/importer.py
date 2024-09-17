import pygame
import csv
import os


def import_csv(path):
    terrain_map = []
    with open(path) as csv_map:
        layout = csv.reader(csv_map, delimiter=',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map


def import_tiles(path):
    surface_map = {}

    for _,_,imgs in os.walk(path):
        for img in imgs:
            full_path = path + '/' + img
            img_surface = pygame.image.load(full_path)
            surface_map[img] = img_surface

    return surface_map
