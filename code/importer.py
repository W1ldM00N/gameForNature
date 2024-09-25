import pygame
import csv
import os
import json


def import_csv(path):
    terrain_map = []
    with open(path) as csv_map:
        layout = csv.reader(csv_map, delimiter=',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map


def import_tiles(path):
    surface_map = {}

    for _, _, imgs in os.walk(path):
        for img in imgs:
            full_path = path + '/' + img
            img_surface = pygame.image.load(full_path)
            surface_map[img] = img_surface

    return surface_map


def import_json(path):
    with open(path) as file:
        data = json.load(file)
    return data


def json_dump(path, data):
    with open(path, "w") as file:
        json.dump(data, file)
