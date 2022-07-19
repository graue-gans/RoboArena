import pygame

#utility functions for the movement and roation
#
#



#rotate a image around it's center
def rotate_at_center(window, image, pos, angle):
    x,y = pos
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft = pos).center)
    window.blit(rotated_image, new_rect.topleft)

#not owrking
#rotate a image around a given position
def rotate_at_pos(window, image, pos, angle):
    x, y = pos
    rotated_image = pygame.transform.rotate(image, angle)
    window.blit(rotated_image, pos)


#add 2 given vectors
def vector_addition(v1 , v2):
    return [v1[0] + v2[0] , v1[0] + v2[1]]

