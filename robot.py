import math
from time import sleep

import pygame

from map_utility import Map
from movement_utility import rot_center

from upload_effects import explosion_effect, player_robot_img, player_gun_img, top_left, top_right, bottom_left, \
    bottom_right


# todo: create a class for the collision and put all collision utility methods in it
class Robot:
    """
    'Abstract' Robot class
    Contains the basic fields and methods for every robot
    """

    def __init__(self, start_position, max_velocity, rotation_velocity, acceleration):
        self.x, self.y = start_position
        self.angle = 0
        self.max_vel = max_velocity
        self.rotation_vel = rotation_velocity
        self.vel = 0
        self.a = acceleration
        self.vel_vector = [0, 0]
        self.robot_image = player_robot_img
        self.robot_gun_image = player_gun_img
        self.save_velocity()

    def save_velocity(self):
        self.saved_vel = self.max_vel
        self.saveed_rotation_vel = self.rotation_vel

    # rotate the robot by adjusting the robot_angle
    def rotate_robot(self, left=False, right=False):

        if left and robot_top_left_corner_col is None and robot_bottom_right_corner_col is None:
            self.angle += self.rotation_vel
        if right and robot_top_right_corner_col is None and robot_bottom_left_corner_col is None:
            self.angle -= self.rotation_vel

    # rotate the image of the robot and its weapon by using movement_utility.py functions
    def draw(self, win, counter):
        win.blit(rot_center(self.robot_image, self.angle), (self.x, self.y))

    # win.blit(rot_center(self.robot_gun_image, self.angle), (self.x+38, self.y+25))

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
    def check_lava_collision(self, mask, win, counter, x=0, y=0):
        global over_lap_point
        robot_img = rot_center(self.robot_image, self.angle)
        robo_mask = pygame.mask.from_surface(robot_img)
        offset = (int(self.x - x), int(self.y - y))
        over_lap_point = mask.overlap(robo_mask, offset)
        over_lap_area = mask.overlap_area(robo_mask, offset)

        if over_lap_area >= 300:
            self.lava_collision()
            win.blit(rot_center(explosion_effect[counter // 16], self.angle),
                     (self.x - 14, self.y - 10))  # draw the explosion animation
        else:
            if water_overlap is None:
                self.max_vel = self.saved_vel

    # detect if there is a collision with the water
    def check_water_collision(self, mask, rect, win):
        global water_overlap
        robot_img = rot_center(self.robot_image, self.angle)

        robo_rect = robot_img.get_rect(topleft=(self.x, self.y))
        robo_mask = pygame.mask.from_surface(robot_img)
        offset = (int(rect[0] - self.x), int(rect[1] - self.y))
        water_overlap = robo_mask.overlap(mask, offset)
        if water_overlap:
            # when collision -> create a surface from the overlap mask
            under_water_mask = robo_mask.overlap_mask(mask, offset)
            under_water_surf = under_water_mask.to_surface().convert_alpha()
            under_water_surf.set_colorkey((0, 0, 0))
            surf_w, surf_h = under_water_surf.get_size()
            # now give a favourite color to each set pixel in the mask
            for x in range(surf_w):
                for y in range(surf_h):
                    if under_water_surf.get_at((x, y))[0] != 0:
                        under_water_surf.set_at((x, y), 'blue')
            win.blit(under_water_surf, robo_rect)
            self.max_vel = 1
        else:
            self.max_vel = self.saved_vel

    # check if there is a collision with wall
    def check_wall_collision(self, mask, x=0, y=0):

        offset = (int(self.x - x), int(self.y - y))
        global robot_top_left_corner_col, robot_top_right_corner_col, robot_bottom_left_corner_col \
            , robot_bottom_right_corner_col
        robot_mask = pygame.mask.from_surface(rot_center(self.robot_image, self.angle))
        poi = mask.overlap(robot_mask, offset)
        # craete mask for each corner of the robot, to know which of it has a collision
        robot_top_left_corner_col = mask.overlap(self.roboter_corner_mask()[0], offset)
        robot_top_right_corner_col = mask.overlap(self.roboter_corner_mask()[1], offset)
        robot_bottom_left_corner_col = mask.overlap(self.roboter_corner_mask()[2], offset)
        robot_bottom_right_corner_col = mask.overlap(self.roboter_corner_mask()[3], offset)

        if poi is not None:
            self.wall_collision(self)

    # what to do if there is a collision with the lava
    def lava_collision(self):
        self.max_vel = 1

    # what to do if there is a collision with the wall
    def wall_collision(self, robot):

        if robot_top_left_corner_col is not None and robot_top_right_corner_col is not None:
            if robot.vel > 0:
                robot.vel = -robot.vel / 2

        elif robot_top_left_corner_col is not None:
            if robot.vel >= 0:
                robot.colide_clock_wise()
            else:
                robot.colide_counter_clock_wise()

        elif robot_top_right_corner_col is not None:
            if robot.vel >= 0:
                robot.colide_counter_clock_wise()
            else:
                robot.colide_clock_wise()

        if robot_bottom_left_corner_col is not None:
            if robot.vel >= 0:
                robot.colide_clock_wise()
            else:
                if robot.vel < 0:
                    robot.vel = -robot.vel / 2

        if robot_bottom_right_corner_col is not None:
            if robot.vel >= 0:
                robot.colide_counter_clock_wise()
            else:
                if robot.vel < 0:
                    robot.vel = -robot.vel / 2

    # utility function for check_wall_collision
    # detect which corner of the robot has a collision
    def roboter_corner_mask(self):
        top_left_mask = pygame.mask.from_surface(rot_center(top_left, self.angle))
        top_right_mask = pygame.mask.from_surface(rot_center(top_right, self.angle))
        bottom_left_mask = pygame.mask.from_surface(rot_center(bottom_left, self.angle))
        bottom_right_mask = pygame.mask.from_surface(rot_center(bottom_right, self.angle))
        return [top_left_mask, top_right_mask, bottom_left_mask, bottom_right_mask]

    # utility function for check_wall_collision
    # detect which wall the robot is in collision with
    def wall_detection(self):
        angle = self.angle % 360
        wall_left = False
        wall_right = False
        wall_bottom = False
        wall_top = False
        if self.vel >= 0:
            if (0 < angle <= 90 and robot_top_left_corner_col is not None) or (
                    90 <= angle < 180 and robot_top_right_corner_col is not None):
                wall_left = True
            if (270 < angle <= 359 and robot_top_left_corner_col is not None) or (
                    0 <= angle < 90 and robot_top_right_corner_col is not None):
                wall_top = True

            if (180 < angle <= 270 and robot_top_left_corner_col is not None) or (
                    270 <= angle < 359 and robot_top_right_corner_col is not None):
                wall_right = True

            if (90 < angle <= 180 and robot_top_left_corner_col is not None) or (
                    180 <= angle < 270 and robot_top_right_corner_col is not None):
                wall_bottom = True
        return [wall_left, wall_top, wall_right, wall_bottom]

    # utility function for check_wall_collision
    # the direction of the movement after the collision with the wall with given angle -> in clock direction
    def colide_clock_wise(self):
        clide_rotation_vel = self.vel
        bounce = self.vel
        if self.wall_detection()[0]:
            self.angle -= clide_rotation_vel
            self.x += bounce
        if self.wall_detection()[1]:
            self.angle -= clide_rotation_vel
            self.y += bounce
        if self.wall_detection()[2]:
            self.angle -= clide_rotation_vel
            self.x -= bounce
        if self.wall_detection()[3]:
            self.angle -= clide_rotation_vel
            self.y -= bounce

    # utility function for check_wall_collision
    # the direction of the movement after the collision with the wall with given angle -> in counter clock direction
    def colide_counter_clock_wise(self):
        clide_rotation_vel = self.vel
        bounce = self.vel
        if self.wall_detection()[0]:
            self.angle += clide_rotation_vel
            self.x += bounce
        if self.wall_detection()[1]:
            self.angle += clide_rotation_vel
            self.y += bounce
        if self.wall_detection()[2]:
            self.angle += clide_rotation_vel
            self.x -= bounce
        if self.wall_detection()[3]:
            self.angle += clide_rotation_vel
            self.y -= bounce


# examplary classes that extend the 'abstract' Robot class
class BasicRobot(Robot):
    pass


class PlayerRobot(Robot):

    def move_robot(self):
        key = pygame.key.get_pressed()
        moving = False
        slowing_down_with_space = False  # its True if the player presses 'space'

        if key[pygame.K_w] and key[pygame.K_s]:
            pass
        # using elif to not allow the player using 2-keys 'w' and 's'

        elif key[pygame.K_w]:
            moving = True
            self.move_forward()

        elif key[pygame.K_s]:
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


class EnemyRobot(Robot):
    pass
