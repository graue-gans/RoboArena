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
        self.vel_vector = [0, 0]
        self.last_moving_direction = -1 #-1 dummy value, 0: forward , 1:backward


    #rotate the robot by adjusting the robot_angle
    def rotate_robot(self,left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        if right:
            self.angle -= self.rotation_vel
    #rotate the weapon by adjust the weapon_angle
    def rotate_weapon(self, left=False, right=False):
        if left:
            self.weapon_angle += self.rotation_vel
        if right:
            self.weapon_angle -= self.rotation_vel

    def draw_robot(self,win,image,gun):
        rotate_center_axis(win, image,(self.x,self.y),self.angle)
        rotate_center_axis(win, gun,(self.x + 20,self.y),self.weapon_angle)
        pygame.display.update()





# examplary classes that extend the 'abstract' Robot class
class BasicRobot(Robot):
    pass

class PlayerRobot(Robot):
    image = pygame.image.load("images/robot.png")
    gun = pygame.image.load("images/Gun_01.png")


    def move_direction(self):
        radians = math.radians(self.angle)
        self.vel_vector[0] = math.cos(radians) * self.vel
        self.vel_vector[1] = math.sin(radians) * self.vel
        self.y -= self.vel_vector[0]
        self.x -= self.vel_vector[1]



    def move_forward(self):
        self.vel = min(self.vel + self.a, self.max_vel)
        self.move_direction()

    def move_backward(self):
        self.vel = max(self.vel - self.a, -self.max_vel/2)
        self.move_direction()

    def deceleration_forward(self):
        self.vel = max(self.vel - self.a * 2, 0)
        self.move_direction()


    def deceleration_backward(self):
        self.vel = min(self.vel + self.a * 2, 0)
        self.move_direction()







class EnemyRobot(Robot):
    pass

