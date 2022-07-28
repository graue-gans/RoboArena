import pygame


def scale_img(img,factor):
    size = round(img.get_width() * factor) , round(img.get_height()*factor)
    return pygame.transform.scale(img,size)


player_robot_img = scale_img(pygame.image.load("images/tank/Hull_04.png"), 0.4)
player_gun_img = scale_img(pygame.image.load("images/Weapon_Color_A/Gun_04.png"),0.5)



explosion_effect = [scale_img(pygame.image.load("images/explosion/Explosion_E.png"),0.5),
                    scale_img(pygame.image.load("images/explosion/Explosion_F.png"),0.5),
                    scale_img(pygame.image.load("images/explosion/Explosion_G.png"),0.5),
                    scale_img(pygame.image.load("images/explosion/Explosion_H.png"),0.5)]