from Shared import *
import pygame
import random


vec = pygame.math.Vector2


class Person:
    def __init__(self, app, pos, number):

        self.app = app
        self.grid_pos = pos
        self.starting_pos = [pos.x, pos.y]
        self.pix_pos = self.get_pix_pos()
        self.radius = int(self.app.cell_width // 2.3)
        self.number = number
        self.colour = self.set_colour()
        self.direction = vec(0, 0)
        self.personality = self.set_personality()
        self.target = None
        self.speed = self.set_speed()


    def get_random_direction(self):
        while True:
            x_dir, y_dir = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])

            next_pos = vec(self.grid_pos.x + x_dir, self.grid_pos.y + y_dir)
            if next_pos not in self.app.walls:
                break
        return vec(x_dir, y_dir)


