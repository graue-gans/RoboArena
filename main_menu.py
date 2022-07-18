import pygame
import sys

from custom_background import custom_background
from game_window import Game_window

width = 1000
height = 1000
pygame.init()
screen = pygame.display.set_mode((1000,1000))
font = pygame.font.SysFont('comic Sans MS',20)
button_aktiv = False
clock = pygame.time.Clock()

def textObjekt(text,font):
    text_rect = font.render(text,True,(100,100,0))
    return text_rect,text_rect.get_rect()

def button(x,y,width,height,color_in_active,color_active,massage):
    global button_aktiv
    if mouse[0] > x and mouse[0] < x + width and mouse[1] > y and mouse[1] < y + height:
        pygame.draw.rect(screen, color_active, (x, y, width, height))
        if click[0] == 1 and button_aktiv == False:
            button_aktiv = True
            if massage == "play":
                robo_arena = Game_window()
            elif massage == "map":
                c_b_1 = custom_background()
            elif massage == "setting":
                sys.exit()
            elif massage == "exit":
                sys.exit()
        if click[0] == 0:
            button_aktiv = False

    else:
        pygame.draw.rect(screen, color_in_active, (x, y, width, height))
    text_k,text_rect = textObjekt(massage,font)
    text_rect.center = ((x + (width/2)), (y + (height/2)))
    screen.blit(text_k,text_rect)


go = True

while go:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    click = pygame.mouse.get_pressed()
    screen.fill((0,0,0))
    mouse = pygame.mouse.get_pos()
    button(350,500,300,80,(127,125,125),(255,255,255),"play")
    button(350, 600, 300, 80, (127,125,125), (255, 255, 255),"map")
    button(350, 700, 300, 80, (127,125,125), (255, 255, 255),"setting")
    button(350, 800, 300, 80, (127, 125, 125), (255, 255, 255), "exit")
    pygame.display.flip()
    clock.tick(60)






