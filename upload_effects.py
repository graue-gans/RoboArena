import pygame


def scale_img(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)


def load(filename):
    image = pygame.image.load(filename)
    return image

player_robot_img = scale_img(load("images/tank_player/Hull_01.png"), 0.3)
top_left = scale_img(load("images/tank_player/collision_check/top_left.png"), 0.3)
top_right = scale_img(load("images/tank_player/collision_check/top_right.png"), 0.3)
bottom_left = scale_img(load("images/tank_player/collision_check/bottom_left.png"), 0.3)
bottom_right = scale_img(load("images/tank_player/collision_check/bottom_right.png"), 0.3)
player_gun_img = scale_img(load("images/Weapon_Color_A/Gun_04.png"), 0.4)

explosion_effect = [scale_img(pygame.image.load("images/explosion/Explosion_E.png"), 0.5),
                    scale_img(pygame.image.load("images/explosion/Explosion_F.png"), 0.5),
                    scale_img(pygame.image.load("images/explosion/Explosion_G.png"), 0.5),
                    scale_img(pygame.image.load("images/explosion/Explosion_H.png"), 0.5)]
