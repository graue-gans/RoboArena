import csv

import pygame

class window():
    width = 1000
    height = 1000
    scale = 10
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    width_tiles = int(width / scale)  # number of tiles
    height_tiles = int(width / scale)
    background = []  # contains all 100x100 tiles, each number represent a tile
    wall = 5

    # load the background from csv into background-variable
    def load_background(self):
        file = open(self.file)
        csvreader = csv.reader(file)
        self.background = []
        for line in csvreader:
            self.background.append([int(x) for x in line])



    #create a csv file and fill it
    def save_current_background_csv(self):
        with open(self.file, 'w', encoding='UTF8',newline='') as f:
            firstline = True
            writer = csv.writer(f)
            writer.writerows(self.background)
        f.close()


    #a empty 2-d-list is needed to be able to load the background from csv-file
    def init_empty_background(self):
        for i in range(self.width_tiles):
            self.background.append([])
            for j in range(self.height_tiles):
                if (i < self.wall or i >= self.width_tiles - self.wall ) or (j < self.wall or j >= self.height_tiles - self.wall):
                    self.background[i].append(2)
                else:
                    self.background[i].append(0)

        # draw a single tile depending on its number
    def draw_tile(self, i, j):
        if self.background[i][j] == 2:
            border_size = 1
        elif self.background[i][j] == 1:
            border_size = 1
        else:
            border_size = 0
        pygame.draw.rect(self.screen, self.tile_set[str(self.background[i][j])],
                         (i * self.scale, j * self.scale, self.scale, self.scale), border_size)

    def render_background(self):
        for i in range(self.width_tiles):
            for j in range(self.width_tiles):
                self.draw_tile(i, j)






