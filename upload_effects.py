import pygame


def scale_img(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)


def load(filename):
    image = pygame.image.load(filename)
    return image


top_left = scale_img(load("images/tank_player/collision_check/top_left.png"), 0.3)
top_right = scale_img(load("images/tank_player/collision_check/top_right.png"), 0.3)
bottom_left = scale_img(load("images/tank_player/collision_check/bottom_left.png"), 0.3)
bottom_right = scale_img(load("images/tank_player/collision_check/bottom_right.png"), 0.3)


player_robot_img = scale_img(load("images/tank_player/Hull_01.png"), 0.3)
player_gun_img = scale_img(load("images/Weapon_Color_A/Gun_04.png"), 0.4)

player_life_image = scale_img(load("images/life.png"), 0.05)


enemy_static_image = scale_img(load("images/tank_enemy/Hull_static_01.png"), 0.3)
enemy_static_gun = scale_img(load("images/Weapon_Color_A/Gun_static_01.png"), 0.4)


enemy_patrol_image = scale_img(load("images/tank_enemy/Hull_01.png"), 0.3)
enemy_patrol_gun = scale_img(load("images/Weapon_Color_A/Gun_patrol_01.png"), 0.4)

enemy_life_image = scale_img(load("images/life.png"), 0.02)

explosion_effect = [scale_img(pygame.image.load("images/explosion/Explosion_E.png"), 0.5),
                    scale_img(pygame.image.load("images/explosion/Explosion_F.png"), 0.5),
                    scale_img(pygame.image.load("images/explosion/Explosion_G.png"), 0.5),
                    scale_img(pygame.image.load("images/explosion/Explosion_H.png"), 0.5)]
