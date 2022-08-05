import pygame


# utility functions for the movement and roation
#
#


# rotate a image around it's center but returns the rotated image (needed for the collision)
def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

#rotate a image and blit it on the screen (needed for the Gun)
def rot_center_gun(image, pos, angle,win):
    """rotate an image while keeping its center"""
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=image.get_rect(topleft=pos).center)
    win.blit(rot_image,rot_rect.topleft)








# add 2 given vectors
def vector_addition(v1, v2):
    return [v1[0] + v2[0], v1[0] + v2[1]]
