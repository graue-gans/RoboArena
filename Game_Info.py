import pygame

from map_utility import Tileset

pygame.font.init()
font1 = pygame.font.SysFont('Comic Sans MS', 20)
font2 = pygame.font.SysFont('Comic Sans MS', 30)
font3 = pygame.font.SysFont('Comic Sans MS', 50)

ts = Tileset()


# show the tiles with its tileoffset to render tiles on custom background screen
def custom_background_Info(window, font, text, rgb):
    # displays a text at the center of the window
    surface = pygame.Surface((300, 300))
    surface.convert_alpha()
    surface.fill((0, 0, 0))

    surface.get_rect(topleft=(100, 100))
    y = 20
    for tile in ts.tiles:
        surface.blit(tile, (200, y))
        y += 50
    y = 10
    for t in text:
        text_surface = font.render(t, False, rgb)
        surface.blit(text_surface, (10, y))
        y += 50
    window.blit(surface, (50, 100))


# show "press Espace" on custom background screen
def custom_background_massage(window, font, text, rgb):
    text_surface = font.render(text, False, rgb)
    window.blit(text_surface, (window.get_width() / 2 - text_surface.get_width() / 2, 100))


# show a text while pausing the game
def pausing_info(window, font, text, rgb):
    text_surface = font.render(text, False, rgb)
    window.blit(text_surface, (window.get_width() / 2 - text_surface.get_width() / 2, 100))


def show_life_player(life_image, window, robot):
    i = 0
    life_images = []
    for j in range(0, int(robot.life)):
        life_images.append(life_image)

    for l in life_images:
        window.blit(l, (i + 20, 10))
        i += 30


def show_life_enemy(life_image, window, robot):
    if len(robot)!= 0:
        i = -10
        life_images = []
        for j in range(0, int(robot[0].life)):
            life_images.append(life_image)

        for l in life_images:
            window.blit(l, (robot[0].x + i, robot[0].y - 15))
            i += 30
