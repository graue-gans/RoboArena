import csv

import pygame




class Map():
    pygame.init()
    width =1000
    height= 1000
    screen = pygame.display.set_mode((width, height))
    scale = 10  # scale a pixel by 10, so we have 10pixel tiles
    FPS = 60  # default FPS=60
    clock = pygame.time.Clock()
    horizontal_tiles = 100  # number of horizontal tiles
    vertical_tiles = 100  # number of vertical tiles
    background = []  # contains all 100x100 tiles, each number represent a tile
    tile_set = {"0": (0, 0, 0), "1": (255, 255, 255),
                "2": (62, 36, 25),
                "3": (140, 124, 213)}  # each tile can have different color. it will be replaced by images later
    pygame.init()

    # load the background from csv into the background-variable
    def load_background(self, file):
        f = open(file)
        csvreader = csv.reader(f)
        self.background = []
        for line in csvreader:
            self.background.append([int(x) for x in line])

    # create a csv file and fill it with tiles; each number represent a tile
    def save_background_csv(self, file):
        with open(file, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(self.background)
        f.close()

    # is needed to reset the map. fill the background with '0' tiles = 'black' tiles
    def init_empty_background(self):
        self.background = []
        for i in range(self.horizontal_tiles):
            self.background.append([])
            for j in range(self.vertical_tiles):
                self.background[i].append(0)

    # save the empty_background so reset the map
    def reset_map(self, file):
        self.init_empty_background()
        self.save_background_csv(file)

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

    # draw all 100x100 tiles by using draw_tile method for every tile
    def render_background(self):
        for i in range(self.horizontal_tiles):
            for j in range(self.vertical_tiles):
                self.draw_tile(i, j)
