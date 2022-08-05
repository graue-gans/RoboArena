import math
from time import sleep

import pygame

from map_utility import Map
from movement_utility import rot_center, rot_center_gun

from upload_effects import explosion_effect, player_robot_img, player_gun_img, top_left, top_right, bottom_left, \
    bottom_right


class Robot:
    """
    'Abstract' Robot class
    Contains the basic fields and methods for every robot
    """

    def __init__(self, start_position, max_velocity, rotation_velocity, acceleration, robo_image, robo_gun_image):
        self.x, self.y = start_position
        self.angle = 0
        self.max_vel = max_velocity
        self.rotation_vel = rotation_velocity
        self.vel = 0
        self.a = acceleration
        self.vel_vector = [0, 0]
        # look at upload_effects.py to upload new images
        self.robot_image = robo_image
        self.robot_gun_image = robo_gun_image

    # rotate the robot by adjusting the robot_angle
    def rotate_robot(self, wall_col, left=False, right=False):

        if left and wall_col.top_left_corner_collision is None and wall_col.bottom_right_corner_collision is None:
            self.angle += self.rotation_vel
        if right and wall_col.top_right_corner_collision is None and wall_col.bottom_left_corner_collision is None:
            self.angle -= self.rotation_vel

    # rotate the image of the robot and its weapon by using movement_utility.py functions
    def draw(self, win, counter, robot, l_col, water_col):
        if l_col.col:
            win.blit(rot_center(explosion_effect[counter // 16], robot.angle),
                     (robot.x - 14, robot.y - 10))  # draw the explosion animation

        win.blit(rot_center(self.robot_image, self.angle), (self.x, self.y))

        # draw the gun
        rot_center_gun(self.robot_gun_image, (self.x + 20, self.y - 3), self.angle, win)

        # draw a new surface of the robot under the water, it sould be drawn after the robot
        if water_col.col:
            win.blit(water_col.under_water_surf, (self.x, self.y))

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


# collision class
class Collision():
    # if there is a Collision
    col = False


class Robot_Projectile_Collision(Collision):
    def robot_projectile_collision(self, projectile, robot):
        robot_img = rot_center(robot.robot_image, robot.angle)
        projectile_img = projectile.image

        # make masks
        robot_mask = pygame.mask.from_surface(robot_img)
        projectile_mask = pygame.mask.from_surface(projectile_img)
        #offset
        offset = (int(projectile.x - robot.x), int(projectile.y - robot.y))
        #overlap point
        overlap_projectile_robot = robot_mask.overlap_area(projectile_mask, offset)

        if overlap_projectile_robot is not None:
            self.col = True
            #what should happen?
        else:
            self.col = False


class Water_Collision(Collision):
    water_vel = 1
    # give the surf of the robot under the water
    under_water_surf = None
    # a Flag to see if the whole robot's body is under the water
    full_under_water = False

    # detect if there is a collision with the water
    def water_Robot_collision(self, water_mask, robot):
        robot_img = rot_center(robot.robot_image, robot.angle)

        robo_mask = pygame.mask.from_surface(robot_img)

        offset = (int(0 - robot.x), int(0 - robot.y))

        water_overlap = robo_mask.overlap(water_mask, offset)
        water_overerlap_area = robo_mask.overlap_area(water_mask, offset)

        # check if the robot is completely under the water:
        if water_overerlap_area == robo_mask.count():
            self.full_under_water = True
            robot.vel = robot.vel / 1.1  # slow down the robot
        else:
            self.full_under_water = False
        # check if there is a collision with water
        if water_overlap:
            self.col = True
            # when collision -> create a surface from the overlap mask
            under_water_mask = robo_mask.overlap_mask(water_mask, offset)
            self.under_water_surf = under_water_mask.to_surface().convert_alpha()
            self.under_water_surf.set_colorkey((0, 0, 0))
            surf_w, surf_h = self.under_water_surf.get_size()
            # now give a favourite color to each set pixel in the mask
            for x in range(surf_w):
                for y in range(surf_h):
                    if self.under_water_surf.get_at((x, y))[0] != 0:
                        self.under_water_surf.set_at((x, y), 'blue')
        else:
            self.col = False


class Lava_Collision(Collision):
    lava_vel = 1
    # a flag to know if the whole body of the robot is on the lavatiles
    full_on_lava = False

    # check if there is a collision between a robot and lava
    def lava_Robot_collision(self, lava_mask, robot, x=0, y=0):
        robot_img = rot_center(robot.robot_image, robot.angle)
        robo_mask = pygame.mask.from_surface(robot_img)
        offset = (int(robot.x - x), int(robot.y - y))
        lava_overlap_area = lava_mask.overlap_area(robo_mask, offset)

        if lava_overlap_area == robo_mask.count():
            self.full_on_lava = True
            robot.vel = robot.vel / 1.1  # slow down the robot
        else:
            self.full_on_lava = False

        # if 200 bits in over_lap_mask is set -> collision is active
        if lava_overlap_area >= 200:
            self.col = True
            robot.vel = robot.vel / 1.03  # slow down
        else:
            self.col = False


class Wall_Collision(Collision):
    # we created 4 masks for each corner of the robot, so we can proof if any corner has a collision
    # these variables just needed for the wall collision
    top_left_corner_collision = None
    top_right_corner_collision = None
    bottom_left_corner_collision = None
    bottom_right_corner_collision = None

    def wall_projectile_collision(self, wall_mask, projectile, x=0, y=0):
        projectile_mask = pygame.mask.from_surface(projectile.image)
        offset = (int(projectile.x - x), int(projectile.x - y))
        overlap_point = wall_mask.overlap(projectile_mask, offset)
        if overlap_point is not None:
            self.col = True
            # what should happen?
            pass
        else:
            self.col = False

    # check if there is a collision with the wall
    def wall_Robot_collision(self, wall_mask, robot, x=0, y=0):

        offset = (int(robot.x - x), int(robot.y - y))
        # create a robot mask to check if there is collision between robot and the wall
        robot_mask = pygame.mask.from_surface(rot_center(robot.robot_image, robot.angle))
        poi = wall_mask.overlap(robot_mask, offset)
        # craete mask for each corner of the robot, to know which of it has a collision
        self.top_left_corner_collision = wall_mask.overlap(self.roboter_corner_mask(robot)[0], offset)
        self.top_right_corner_collision = wall_mask.overlap(self.roboter_corner_mask(robot)[1], offset)
        self.bottom_left_corner_collision = wall_mask.overlap(self.roboter_corner_mask(robot)[2], offset)
        self.bottom_right_corner_collision = wall_mask.overlap(self.roboter_corner_mask(robot)[3], offset)
        # what to do if  there is collision with the wall
        if poi is not None:
            self.wall_collision(robot)

    # what to do if there is a collision with the wall
    def wall_collision(self, robot):
        if self.top_left_corner_collision is not None and self.top_right_corner_collision is not None:
            if robot.vel > 0:
                robot.vel = -robot.vel / 2

        elif self.top_left_corner_collision is not None:
            if robot.vel >= 0:
                self.colide_clock_wise(robot)
            else:
                self.colide_counter_clock_wise(robot)

        elif self.top_right_corner_collision is not None:
            if robot.vel >= 0:
                self.colide_counter_clock_wise(robot)
            else:
                self.colide_clock_wise(robot)

        if self.bottom_left_corner_collision is not None:
            if robot.vel >= 0:
                self.colide_clock_wise(robot)
            else:
                if robot.vel < 0:
                    robot.vel = -robot.vel / 2

        if self.bottom_right_corner_collision is not None:
            if robot.vel >= 0:
                self.colide_counter_clock_wise(robot)
            else:
                if robot.vel < 0:
                    robot.vel = -robot.vel / 2

    # create the 4 masks for each corner and return them in a list
    def roboter_corner_mask(self, robot):
        top_left_mask = pygame.mask.from_surface(rot_center(top_left, robot.angle))
        top_right_mask = pygame.mask.from_surface(rot_center(top_right, robot.angle))
        bottom_left_mask = pygame.mask.from_surface(rot_center(bottom_left, robot.angle))
        bottom_right_mask = pygame.mask.from_surface(rot_center(bottom_right, robot.angle))
        return [top_left_mask, top_right_mask, bottom_left_mask, bottom_right_mask]

    # detects based on the angle and the collison-corner which wall the robot is collision with: left right top or bottom
    def wall_detection(self, robot):
        angle = robot.angle % 360
        wall_left = False
        wall_right = False
        wall_bottom = False
        wall_top = False
        if robot.vel >= 0:
            if (0 < angle <= 90 and self.top_left_corner_collision is not None) or (
                    90 <= angle < 180 and self.top_right_corner_collision is not None):
                wall_left = True
            if (270 < angle <= 359 and self.top_left_corner_collision is not None) or (
                    0 <= angle < 90 and self.top_right_corner_collision is not None):
                wall_top = True

            if (180 < angle <= 270 and self.top_left_corner_collision is not None) or (
                    270 <= angle < 359 and self.top_right_corner_collision is not None):
                wall_right = True

            if (90 < angle <= 180 and self.top_left_corner_collision is not None) or (
                    180 <= angle < 270 and self.top_right_corner_collision is not None):
                wall_bottom = True
        return [wall_left, wall_top, wall_right, wall_bottom]

    # utility function for check_wall_collision
    # the direction of the movement after the collision with the wall with given angle -> in clock direction
    def colide_clock_wise(self, robot):
        clide_rotation_vel = robot.vel
        bounce = robot.vel
        if self.wall_detection(robot)[0]:
            robot.angle -= clide_rotation_vel
            robot.x += bounce
        if self.wall_detection(robot)[1]:
            robot.angle -= clide_rotation_vel
            robot.y += bounce
        if self.wall_detection(robot)[2]:
            robot.angle -= clide_rotation_vel
            robot.x -= bounce
        if self.wall_detection(robot)[3]:
            robot.angle -= clide_rotation_vel
            robot.y -= bounce

    # utility function for check_wall_collision
    # the direction of the movement after the collision with the wall with given angle -> in counter clock direction
    def colide_counter_clock_wise(self, robot):
        clide_rotation_vel = robot.vel
        bounce = robot.vel
        if self.wall_detection(robot)[0]:
            robot.angle += clide_rotation_vel
            robot.x += bounce
        if self.wall_detection(robot)[1]:
            robot.angle += clide_rotation_vel
            robot.y += bounce
        if self.wall_detection(robot)[2]:
            robot.angle += clide_rotation_vel
            robot.x -= bounce
        if self.wall_detection(robot)[3]:
            robot.angle += clide_rotation_vel
            robot.y -= bounce


# examplary classes that extend the 'abstract' Robot class
class BasicRobot(Robot):
    pass


class PlayerRobot(Robot):
    def move_robot(self, wall_col):
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
            self.rotate_robot(wall_col, right=True)

        if key[pygame.K_a]:
            self.rotate_robot(wall_col, left=True)

        # ----------------------------------------------
        # slow down the robot when the player doesn't speed up up/backwards and when the player doesn't slow down with the 'space'-key

        if not moving and self.vel >= 0 and not slowing_down_with_space:
            self.deceleration_forward(1 / 2)

        if not moving and self.vel < 0 and not slowing_down_with_space:
            self.deceleration_backward(1 / 2)


class EnemyRobot(Robot):
    pass
