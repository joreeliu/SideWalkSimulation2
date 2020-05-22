import pygame
import os
from Shared.GameConstants import MAP_DAT


def load_image(path, size):
    return pygame.transform.scale(pygame.image.load(path), size)


def load_map():
    rows = 0
    cols = 0

    with open(os.path.join("Assets", "levels", MAP_DAT), 'r') as file:
        for yidx, line in enumerate(file):
            rows += 1
            cols = 0
            for xidx, char in enumerate(line):
                cols += 1

    return rows, cols