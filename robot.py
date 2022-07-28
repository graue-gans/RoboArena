import math
from numpy.linalg import norm
from time import sleep


import pygame

from movement_utility import rot_center
from screen import Screen
from upload_effects import explosion_effect, player_robot_img


class Projectile():
    def __init__(self, x, y, angle, v, filename):
        self.x = x
        self.y = y
        self.angle_rad = math.radians(angle + 90)
        self.dir = self.vec_mult((math.cos(self.angle_rad), math.sin(self.angle_rad)), v)
        self.img = pygame.image.load(filename)

    def vec_mult(self, vec, c):
        return (vec[0]*c, vec[1]*c)

    def draw(self, screen):
        screen.blit(self.img, self.img.get_rect(center = (self.x, self.y)))

    def move(self):
        self.x -= self.dir[0]
        self.y -= self.dir[1]


left_pixel = 0
right_pixel = 0
class Robot(Screen):
    """
    'Abstract' Robot class
    Contains the basic fields and methods for every robot
    """


    def __init__(self, start_position, max_velocity, rotation_velocity, acceleration, robot_image, robot_gun_image):
        self.x, self.y = start_position
        self.angle = 0
        self.max_vel = max_velocity
        self.rotation_vel = rotation_velocity
        self.vel = 0
        self.a = acceleration
        self.vel_vector = [0, 0]
        self.robot_image = robot_image
        self.robot_gun_image = robot_gun_image
        self.projectiles = []
        self.explosion_counter = 0
        self.lava_collision_check = False
        self.wall_collision_check = False


    # rotate the robot by adjusting the robot_angle
    def rotate_robot(self, left=False, right=False):
            if left:
                self.angle += self.rotation_vel
            if right:
                self.angle -= self.rotation_vel
            self.angle %= 360



    # rotate the image of the robot and its weapon by using movement_utility.py functions
    def draw(self, win, counter):
        if self.lava_collision_check and abs(self.vel) > 0:
            win.blit(rot_center(explosion_effect[counter//15], self.angle), (self.x-10, self.y-10)) #draw the explosion animation

        win.blit(rot_center(self.robot_image, self.angle), (self.x, self.y))
        win.blit(rot_center(self.robot_gun_image, self.angle), (self.x+22, self.y+22))




    # find the movement-direction for a given angle and move the robot
    def movement_direction(self):
        radians = math.radians(self.angle)
        self.vel_vector[0] = math.cos(radians) * self.vel
        self.vel_vector[1] = math.sin(radians) * self.vel
        self.y -= self.vel_vector[0]
        self.x -= self.vel_vector[1]

    # add the acceleration to the current velocity of the robot, up to the max-velocity -> positive velocity is a forward movement
    def move_forward(self):
        self.vel = min(self.vel + self.a, self.max_vel)
        self.movement_direction()

    # subtract the acceleration from the current velocity of the robot to -max_velocity -> negative velocity is a backward movement
    def move_backward(self):
        self.vel = max(self.vel - self.a, -self.max_vel / 2)
        self.movement_direction()

    # slow down the robot in forward movement with a given velocity
    def deceleration_forward(self, intensity):
        self.vel = max(self.vel - self.a * intensity, 0)
        self.movement_direction()

    # slow down the robot in backward movement with a given velocity
    def deceleration_backward(self, intensity):
        self.vel = min(self.vel + self.a * intensity, 0)
        self.movement_direction()

    # check if there is a collision with lava
    def colision_check_lava(self, mask, x=0, y=0):
        robot_img =  rot_center(self.robot_image, self.angle)
        robo_mask = pygame.mask.from_surface(robot_img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap_area(robo_mask, offset)
        if poi >= 300:
            self.lava_collision()
        else:
            self.lava_collision_check = False
            self.max_vel = 2


    def shoot(self, screen, v = 6, filename = "images/default_projectile.jpg"):
        p = Projectile(self.x + 38, self.y + 70, self.weapon_angle, v, filename)
        p.draw(screen)
        self.projectiles.append(p)


    # check if there is a collision with wall
    def colision_check_wall(self, mask,counter, x=0, y=0):
        global collision_pixel
        robot_img = rot_center(self.robot_image, self.angle)
        robo_mask = pygame.mask.from_surface(robot_img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(robo_mask, offset)
        collision_pixel = mask.overlap_area(robo_mask, offset)
        if poi is not None:
            self.wall_collision(counter)
        else:
            self.wall_collision_check = False
            
    # what todo if there is a collision with the lava
    def lava_collision(self):
          self.lava_collision_check = True
          self.max_vel = 1


    # what todo if there is a collision with the wall
    #todo is to lock the rotation, if the rotation cause a collision
    def wall_collision(self,counter):
        self.vel = -self.vel


    def update_projectiles(self, screen):
        for p in self.projectiles:
            p.move()
            p.draw(screen)


    def act(self, screen = None):
        pass




# EnemyRobot is static and shoots periodically
class EnemyRobot(Robot):
    def __init__(self, start_position, angle, robot_image, robot_gun_image, firing_speed = 3000):
        self.x, self.y = start_position
        self.robot_image = robot_image
        self.robot_gun_image = robot_gun_image
        self.firing_speed = firing_speed
        self.angle = angle
        self.weapon_angle = angle
        self.t = 0
        self.colision = False
        self.projectiles = []
        self.vel = 0
        self.vel_vector = [0, 0]
        self.explosion_counter = 0
        self.lava_collision_check = False
        self.wall_collision_check = False

    def move_robot(self):
        self.movement_direction()

    def act(self, screen):
        self.shoot(screen)


# PatrolRobot has a static path where it patrols, if player is detected it stop and starts shooting
class PatrolRobot(Robot):
    def __init__(self, start_position, max_velocity, rotation_velocity, acceleration,robot_image, robot_gun_image, xlim, ylim):
        self.x, self.y = start_position
        self.angle = 180
        self.weapon_angle = 180
        self.max_vel = max_velocity
        self.rotation_vel = rotation_velocity
        self.vel = 0
        self.a = acceleration
        self.vel_vector = [0, 0]
        self.robot_image = robot_image
        self.robot_gun_image = robot_gun_image
        self.projectiles = []
        self.moving = True
        self.xlim = xlim
        self.ylim = ylim
        self.explosion_counter = 0
        self.lava_collision_check = False
        self.wall_collision_check = False

    def move_robot(self):
        if self.moving:
            self.move_forward()
            if self.xlim[0] < self.x < self.xlim[1] or self.ylim[0] < self.y < self.ylim[1]:
                self.angle = (self.angle + 180) % 360
                self.weapon_angle = self.angle

    def act(self, screen, pos):
        width = 100  # width of image, FIXME
        detection = False
        if self.angle == 270:
            detection = self.x < pos[0] < self.x + 100 and self.y - width/2 < pos[1] < self.y + width/2
        elif self.angle == 90:
            detection = self.x > pos[0] > self.x - 100 and self.y - width/2 < pos[1] < self.y + width/2
        elif self.angle == 0:
            detection = self.x - width/2 < pos[0] < self.x + width/2 and self.y > pos[1] > self.y - 100
        elif self.angle == 180: 
            detection = self.x - width/2 < pos[0] < self.x + width/2 and self.y < pos[1] < self.y + 100

        if detection:
            self.moving = False
            self.shoot(screen)
        else:
            self.moving = True



class BossRobot(Robot):
    pass


class PlayerRobot(Robot):

    def move_robot(self):
        key = pygame.key.get_pressed()
        moving = False
        slowing_down_with_space = False  # its True if the player presses 'space'

        if key[pygame.K_w] and key[pygame.K_s]:
            pass
        # using elif to not allow the player using 2-keys 'w' and 's'

        if key[pygame.K_w]:
            moving = True
            self.move_forward()

        if key[pygame.K_s]:
            moving = True
            self.move_backward()
        # ------------------------------------------------------
        # slow down the robot with a higher intensity when the player presses 'space'
        if key[pygame.K_w] and key[pygame.K_SPACE] or key[pygame.K_s] and key[pygame.K_SPACE]:
            pass

        elif key[pygame.K_SPACE]:
            slowing_down_with_space = True
            if self.vel >= 0:
                self.deceleration_forward(2)  # 2 is the decelereations intensity
            else:
                self.deceleration_backward(2)

        # -----------------------------------------------
        # rotation of the robot and it's weapon
        if key[pygame.K_d]:
            self.rotate_robot(right=True)

        if key[pygame.K_a]:
            self.rotate_robot(left=True)

        # ----------------------------------------------
        # slow down the robot when the player doesn't speed up up/backwards and when the player doesn't slow down with the 'space'-key

        if not moving and self.vel >= 0 and not slowing_down_with_space:
            self.deceleration_forward(1 / 2)

        if not moving and self.vel < 0 and not slowing_down_with_space:
            self.deceleration_backward(1 / 2)
