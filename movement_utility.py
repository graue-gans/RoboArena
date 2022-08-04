import pygame


# utility functions for the movement and roation
#
#


# rotate a image around it's center
def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image







# add 2 given vectors
def vector_addition(v1, v2):
    return [v1[0] + v2[0], v1[0] + v2[1]]
