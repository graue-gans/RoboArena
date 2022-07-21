import csv
import pygame
from screen import Screen


class Tileset:
    def __init__(self): 
        self.tiles = [self.load('tiles/lava.jpg'), self.load('tiles/stone.jpg'), self.load('tiles/wall.jpg')]

    def load(self, filename):
        image = pygame.image.load(filename)
        return image  #, image.get_rect()


class Map(Screen):
    main_map = 'maps/background.csv'
    custom_map = 'maps/custom_background.csv'




    def __init__(self, tile_size = 20, horizontal_tiles = 50, vertical_tiles = 50):
        self.tile_size = tile_size  
        self.horizontal_tiles = horizontal_tiles  
        self.vertical_tiles   = vertical_tiles
        self.background = []  # contains all tiles, each number represent a type of tile
        self.ts = Tileset()
        self.load_background(self.custom_map)
        BLACK = (0, 0, 0)
        self.transparent_screen = pygame.Surface((self.width, self.height))
        self.transparent_screen.set_colorkey(BLACK)
        BLACK = (0, 0, 0)
        self.transparent_screen = pygame.Surface((self.width, self.height))
        self.transparent_screen.set_colorkey(BLACK)



    # load the csv file and create numeric background
    def load_background(self, file):
        self.background=[]
        f = open(file)
        csvreader = csv.reader(f)
        for line in csvreader:
            self.background.append([int(x) for x in line])

    # draw all tiles by using draw_tile method for every tile
    def render_background(self, screen):
        for i in range(self.vertical_tiles):
            for j in range(self.horizontal_tiles):
                k = self.background[i][j]
                if k >= 3: k = 2
                tile = self.ts.tiles[k]
                screen.blit(tile, (j * self.tile_size, i * self.tile_size))

    # create a csv file and fill it with tiles; each number represent a tile
    def save_background_csv(self, file):
        with open(file, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(self.background)
        f.close()

    # is needed to reset the map. fill the background with '0' = 'lava' tiles
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

    #place the needed tiles on a trasparent screen
    def create_tile_mask(self, surface, tile_offset):
        BLACK = (0, 0, 0)
        self.transparent_screen = pygame.Surface((self.width, self.height))
        self.transparent_screen.set_colorkey(BLACK)
        for i in range(self.horizontal_tiles):
            for j in range(self.vertical_tiles):
                if self.background[i][j] == tile_offset:
                    tile = self.ts.tiles[tile_offset]
                    surface.blit(tile, (j * self.tile_size, i * self.tile_size))
        return pygame.mask.from_surface(surface)
    #make a lava_mask
    def lava_mask(self):
        return self.create_tile_mask(self.transparent_screen, 0)
    #make a wall_mask
    def wall_mask(self):
        return self.create_tile_mask(self.transparent_screen, 2)




