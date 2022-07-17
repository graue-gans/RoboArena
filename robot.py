import math

import pygame

from movement_utility import rotate_center_axis,vektor_addition,rotate_bottom_left
class Robot():
    """
    'Abstract' Robot class
    Contains the basic fields and methods for every robot
    """

    def __init__(self, pos, max_vel, rotation_vel, a):
        self.x, self.y = pos
        self.angle = 0
        self.weapon_angle = 0
        self.max_vel = max_vel
        self.rotation_vel = rotation_vel
        self.vel = 0
        self.a = a
        self.current_move = "stop" #stop, forwards, backwards, neutral
        self.vel_vector = [0, 0]



    def rotate_robot(self,left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        if right:
            self.angle -= self.rotation_vel

    def rotate_weapon(self, left=False, right=False):
        if left:
            self.weapon_angle += self.rotation_vel
        if right:
            self.weapon_angle -= self.rotation_vel

    def draw_robot(self,win,image,gun):

        rotate_center_axis(win, image,(self.x,self.y),self.angle)
        rotate_bottom_left(win, gun,(self.x + 20,self.y),self.weapon_angle)
        pygame.display.update()





# examplary classes that extend the 'abstract' Robot class
class BasicRobot(Robot):
    pass

class PlayerRobot(Robot):
    image = pygame.image.load("images/robot.png")
    gun = pygame.image.load("images/Gun_01.png")

    def move_robot(self,last_move):
        if self.current_move == "backwards":
            self.vel = min(self.vel + self.a/2, self.max_vel/2)
        elif self.current_move == "forwards":
            self.vel = min(self.vel + self.a/2, self.max_vel)
        self.move_direction(last_move)


    def move_direction(self,last_move):
        radians = math.radians(self.angle)
        self.vel_vector[0] = math.cos(radians) * self.vel
        self.vel_vector[1] = math.sin(radians) * self.vel
        if last_move == "forwards":
            self.y -= self.vel_vector[0]
            self.x -= self.vel_vector[1]
        elif last_move == "backwards":
            self.y += self.vel_vector[0]
            self.x += self.vel_vector[1]


    def deceleration(self,last_move):
        self.vel = max(self.vel - self.a * 2, 0)
        self.move_direction(last_move)

    def change_direction_detection(self,last_move):
        if last_move != self.current_move and self.vel != 0:
            return True






class EnemyRobot(Robot):
    pass

