import pygame
import sys
import numpy as np
import copy
import cv2
from Shared import *
from People import *
import fileinput
import random
from Shared.Utilities import load_map


pygame.init()
vec = pygame.math.Vector2



class App:
    def __init__(self):
        self.walls = []
        self.roads = []
        self.people = []
        self.e_pos = []

        self.load()


        self.screen = pygame.display.set_mode((self.map_width, self.map_height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'


        self.cell_width = 1
        self.cell_height = 1
        self.make_people()

    def start_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'
        self.state = 'playing'

    def start_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('PUSH SPACE BAR', self.screen, [
                       self.map_width//2, self.map_height//2-50], START_TEXT_SIZE, (170, 132, 58), START_FONT, centered=True)
        pygame.display.update()

    def draw_text(self, words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0]-text_size[0]//2
            pos[1] = pos[1]-text_size[1]//2
        screen.blit(text, pos)

    def load(self):
        self.background = pygame.image.load(os.path.join("Assets", MAP_PIC))
        img = cv2.imread(os.path.join("Assets", MAP_PIC), 0)
        gaussian_blur_img = cv2.GaussianBlur(img, (5, 5), 0)
        cv2.imwrite('gaussian_blur_img.jpg', gaussian_blur_img)

        self.map_width = img.shape[1]
        self.map_height = img.shape[0]
        gaussian_blur_img[gaussian_blur_img != 0] = 1
        np.savetxt(os.path.join("Assets", "levels", MAP_DAT),  gaussian_blur_img, '%d', '')

        ##self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))

        pbirth_places = []

        with open(os.path.join("Assets", "levels", MAP_DAT), 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "0":
                        self.walls.append(vec(xidx, yidx))
                    elif char != "0":
                        self.roads.append(vec(xidx, yidx))
                        pbirth_places.append(vec(xidx, yidx))

        self.e_pos = random.choices(pbirth_places, k=PEOPLE_NUMBER)

    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    def start_update(self):
        pass

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def playing_update(self):
        for person in self.people:
            person.update()

    def draw_roads(self):
        for road in self.roads:
            pygame.draw.circle(self.screen, (124, 123, 7),
                               (int(road.x*self.cell_width)+self.cell_width//2+TOP_BOTTOM_BUFFER//2,
                                int(road.y*self.cell_height)+self.cell_height//2+TOP_BOTTOM_BUFFER//2), 5)

    def draw_walls(self):
        for wall in self.walls:
            pygame.draw.rect(self.background, (122, 55, 163),
                                (wall.x*self.cell_width, wall.y*self.cell_height, self.cell_width,self.cell_height))


    def make_people(self):
        for idx, pos in enumerate(self.e_pos):
            self.people.append(Person(self, pos, 2))

    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER//2, TOP_BOTTOM_BUFFER//2))
       # self.draw_roads()
        self.draw_walls()

        for person in self.people:
            person.draw()

        pygame.display.update()

    def reset(self):

        for person in self.people:
            person.grid_pos = vec(person.starting_pos)
            person.pix_pos = person.get_pix_pos()
            person.direction *= 0

        self.roads = []
        with open(os.path.join("Assets", "levels", MAP_DAT), 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == '0':
                        self.roads.append(vec(xidx, yidx))

        self.state = "playing"


