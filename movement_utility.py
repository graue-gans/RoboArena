import pygame


def rotate_center_axis(window, image, pos, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft = pos).center)
    window.blit(rotated_image, new_rect.topleft)

def rotate_bottom_left(window, image, pos, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    window.blit(rotated_image, pos)

def vektor_addition(v1 , v2):
    return [v1[0] + v2[0] , v1[0] + v2[1]]

