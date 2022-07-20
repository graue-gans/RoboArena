import csv
import pygame
from screen import Screen


class Tileset:
    def __init__(self): 
        self.tiles = [self.load('tiles/lava.jpg'), self.load('tiles/stone.jpg'), self.load('tiles/stone.jpg')]

    def load(self, filename):
        image = pygame.image.load(filename)
        return image  #, image.get_rect()


class Map(Screen):
    def __init__(self, tile_size = 20, horizontal_tiles = 50, vertical_tiles = 50):
        self.tile_size = tile_size  
        self.horizontal_tiles = horizontal_tiles  
        self.vertical_tiles   = vertical_tiles
        self.background = []  # contains all tiles, each number represent a type of tile
        self.ts = Tileset()

    # load the csv file and create numeric background
    def load_background(self, file):
        f = open(file)
        csvreader = csv.reader(f)
        for line in csvreader:
            self.background.append([int(x) for x in line])

    # draw all tiles by using draw_tile method for every tile
    def render_background(self, screen):
        screen.fill((0, 0, 0))
        for i in range(self.vertical_tiles):
            for j in range(self.horizontal_tiles):
                tile = self.ts.tiles[self.background[i][j]]
                screen.blit(tile, (j * self.tile_size, i * self.tile_size))

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
