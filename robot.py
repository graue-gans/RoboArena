from distutils.command.bdist import show_formats
import math
from numpy.linalg import norm
import numpy as np
from time import sleep
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

import pygame

from map_utility import Map
from movement_utility import rot_center, rot_center_gun

from upload_effects import explosion_effect, player_robot_img, player_gun_img, top_left, top_right, bottom_left, \
    bottom_right


class Projectile():
    def __init__(self, x, y, angle, v, filename):
        self.x = x
        self.y = y
        self.angle_rad = math.radians(angle + 90 % 360)
        self.dir = self.vec_mult((math.cos(self.angle_rad), math.sin(self.angle_rad)), v)
        self.img = pygame.image.load(filename)

    def vec_mult(self, vec, c):
        return (vec[0]*c, vec[1]*c)

    def draw(self, screen):
        screen.blit(self.img, self.img.get_rect(center = (self.x, self.y)))

    def move(self):
        self.x -= self.dir[0]
        self.y -= self.dir[1]


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
        self.projectiles = []

    # rotate the robot by adjusting the robot_angle
    def rotate_robot(self, wall_col, left=False, right=False):
        if left and wall_col.top_left_corner_collision is None and wall_col.bottom_right_corner_collision is None:
            self.angle += self.rotation_vel
        if right and wall_col.top_right_corner_collision is None and wall_col.bottom_left_corner_collision is None:
            self.angle -= self.rotation_vel
        # self.angle %= 360 missing ?

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
        self.vel_vector = (math.cos(radians) * self.vel, math.sin(radians) * self.vel)
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

    # shoot projectiles
    def shoot(self, screen, v = 6, filename = "images/default_projectile.png", angle = None):
        if angle is None: angle = self.angle
        p = Projectile(self.x + 38, self.y + 70, angle, v, filename)  # FIXME projectile offset
        p.draw(screen)
        self.projectiles.append(p)

    # update all projectiles in list
    def update_projectiles(self, screen):
        for p in self.projectiles:
            p.move()
            p.draw(screen)

    # undefined act method for safety
    def act(self, screen = None):
        pass


# collision class
class Collision():
    # if there is a Collision
    col = False


class Robot_Projectile_Collision(Collision):
    def robot_projectile_collision(self, projectile, robot):
        self.col = False
        robot_img = rot_center(robot.robot_image, robot.angle)
        projectile_img = projectile.img

        # make masks
        robot_mask = pygame.mask.from_surface(robot_img)
        projectile_mask = pygame.mask.from_surface(projectile_img)
        #offset
        offset = (int(projectile.x - robot.x), int(projectile.y - robot.y))
        #overlap point
        overlap_projectile_robot = robot_mask.overlap_area(projectile_mask, offset)

        if overlap_projectile_robot is not None:
            self.col = True
            # FIXME subtract health points and check if player died
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
        self.col = False
        
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
    full_on_lava = False

    def lava_Robot_collision(self, lava_mask, robot, x=0, y=0):
        self.col = False
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
    projectile_collision = False

    def wall_projectile_collision(self, wall_mask, projectile, x=0, y=0):
        projectile_mask = pygame.mask.from_surface(projectile.image)
        offset = (int(projectile.x - x), int(projectile.y - y))
        overlap_point = wall_mask.overlap(projectile_mask, offset)
        if overlap_point is not None:
            self.projectile_collision = True
            # what should happen?
            pass
        else:
            self.projectile_collision = False

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


# StaticRobot is static and shoots periodically
class StaticRobot(Robot):
    def __init__(self, start_position, angle, robot_image, robot_gun_image, firing_speed = 3000):
        # FIXME what fields do we really need
        self.x, self.y = start_position
        self.angle = angle
        self.max_vel = 0
        self.rotation_vel = 0
        self.vel = 0
        self.a = 0
        self.vel_vector = [0, 0]
        self.robot_image = robot_image
        self.robot_gun_image = robot_gun_image
        self.projectiles = []
        self.firing_speed = firing_speed

    def move_robot(self):
        # self.movement_direction()
        pass  # FIXME if pass doesnt do it

    def act(self, screen):
        self.shoot(screen)


# PatrolRobot has a static path where it patrols, if player is detected it stop and starts shooting
class PatrolRobot(Robot):
    def __init__(self, start_position, angle, max_velocity, rotation_velocity, acceleration, robot_image, robot_gun_image, xlim, ylim):
        self.x, self.y = start_position
        self.angle = angle
        self.max_vel = max_velocity
        self.rotation_vel = rotation_velocity
        self.vel = 2  # FIXME maybe
        self.a = acceleration
        self.vel_vector = [0, 0]
        self.robot_image = robot_image
        self.robot_gun_image = robot_gun_image
        self.projectiles = []
        self.moving = True
        self.xlim = xlim
        self.ylim = ylim
        self.rotated = False

    def move_robot(self):  # FIXME smoother rotation to come
        if self.moving:
            self.move_forward()
            if not (self.xlim[0] < self.x < self.xlim[1] and self.ylim[0] < self.y < self.ylim[1]) and not self.rotated:
                self.angle = (self.angle + 180) % 360
                self.rotated = True
            elif (self.xlim[0] < self.x < self.xlim[1] and self.ylim[0] < self.y < self.ylim[1]) and self.rotated:
                self.rotated = False

    def act(self, screen, pos, shooting):
        width = 100  # width of image, FIXME
        range = 400
        detection = False
        if self.angle == 270:
            detection = self.x < pos[0] < self.x + range and self.y - width/2 < pos[1] < self.y + width/2
        elif self.angle == 90:
            detection = self.x > pos[0] > self.x - range and self.y - width/2 < pos[1] < self.y + width/2
        elif self.angle == 0:
            detection = self.x - width/2 < pos[0] < self.x + width/2 and self.y > pos[1] > self.y - range
        elif self.angle == 180: 
            detection = self.x - width/2 < pos[0] < self.x + width/2 and self.y < pos[1] < self.y + range

        if detection:
            self.moving = False
            if shooting: self.shoot(screen)
        else:
            self.moving = True


class BossRobot(Robot):
    def __init__(self, start_position, angle, max_velocity, acceleration, robo_image, bg, player_pos):
        self.x, self.y = start_position
        self.angle = angle
        self.old_angle = angle
        self.max_vel = max_velocity
        self.vel = 2
        self.a = acceleration
        self.vel_vector = [0, 0]
        # look at upload_effects.py to upload new images
        self.robot_image = robo_image
        self.projectiles = []
        self.grid = None
        self.edges = []
        self.player_pos = player_pos
        self.transform_background(bg)
        self.find_path(player_pos)
        self.compute_edges()
        self.vel_vector = (self.edges[0][0] - self.x, self.edges[0][1] - self.y)
        self.set_angle()

    def move_robot(self):
        # compute direction and speed
        if self.edges[0][0] - 5 < self.x < self.edges[0][0] + 5 or self.edges[0][1] - 5 < self.y < self.edges[0][1] + 5:
            if len(self.edges) > 1: self.edges.pop(0)
            self.vel_vector = (self.edges[0][0] - self.x, self.edges[0][1] - self.y)
            # self.vel_vector = self.vec_mult(self.vel_vector, (1/norm(self.vel_vector)) * self.vel)
            self.old_angle = self.angle
            self.set_angle()
        self.move_forward()

    def act(self, screen, player_pos, flag = False, shooting = False):
        if norm((self.player_pos[0] - player_pos[0], self.player_pos[1] - player_pos[1])) > 100 or flag:
            self.vel = 2
            self.player_pos = player_pos
            self.find_path(self.player_pos)
            if len(self.path) > 1:
                self.compute_edges()
            else:
                self.edges = [self.player_pos]
            self.vel_vector = (self.edges[0][0] - self.x, self.edges[0][1] - self.y)
            # self.vel_vector = self.vec_mult(self.vel_vector, (1/norm(self.vel_vector)) * self.vel)
            self.old_angle = self.angle
            self.set_angle()
        if len(self.edges) <= 2 and shooting:  # should never be less than 2 
            self.vel = 0
            self.shoot(screen, angle=self.angle + 180 % 360)

    def find_path(self, target_pos):
        if self.grid is not None: self.grid.cleanup

        self.grid = Grid(50, 50, matrix = self.map)
        start = self.grid.node(math.floor(self.x/20), math.floor(self.y/20))
        end   = self.grid.node(math.floor(target_pos[0]/20), math.floor(target_pos[1]/20))

        finder = AStarFinder(diagonal_movement = DiagonalMovement.always)
        self.path, _ = finder.find_path(start, end, self.grid)

    def compute_edges(self):
        self.edges = []
        # self.egdes.append(self.convert_to_coordinates(self.path[0]))
        diff = (self.path[1][0] - self.path[0][0], self.path[1][1] - self.path[0][1])
        for k in range(1, len(self.path) - 1):
            vec = (self.path[k + 1][0] - self.path[k][0], self.path[k + 1][1] - self.path[k][1])
            if diff != vec:
                self.edges.append(self.convert_to_coordinates(self.path[k]))
                diff = vec
        # self.edges.append(self.convert_to_coordinates(self.path[-1]))
        self.edges.append(self.player_pos)

    def transform_background(self, bg):
        n = len(bg)
        m = len(bg[0])

        self.map = [[0] * m for _ in range(n)]
        for i in range(n):
            for j in range(m):
                x = bg[i][j]
                if x == 0:
                    self.map[i][j] = 10
                elif x == 1:
                    self.map[i][j] = 1
                elif x == 2:
                    self.map[i][j] = 0
                elif x in [3, 4]:
                    self.map[i][j] = 4
                elif x == 5:
                    self.map[i][j] = 1

        for i in range(n):
            for j in range(m):
                x = bg[i][j]
                if x == 2:
                    assert(self.map[i][j] == 0)
                    for a in range(-2, 3):
                        for b in range(-2, 3):
                            y = i + a
                            x = j + b
                            if x < 0 or y < 0 or x >= m or y >= n: continue
                            else: 
                                if self.map[i + a][j + b] != 0: self.map[i + a][j + b] = 0

    def create_grid(self, map):
        self.grid = Grid(matrix = map)

    def convert_to_coordinates(self, pos):
        return (10 + 20 * pos[0], 10 + 20 * pos[1])

    def set_angle(self):
        self.angle = round(np.arctan2(self.vel_vector[0], self.vel_vector[1]) * 180 / math.pi * -1 % 360)

    def vec_mult(self, v, k):
        return (v[0] * k, v[1] * k)

    # find the movement-direction for a given angle and move the robot
    def movement_direction(self):
        radians = math.radians(self.angle + 90 % 360)
        self.vel_vector = (math.cos(radians) * self.vel, math.sin(radians) * self.vel)
        self.y += self.vel_vector[1]
        self.x += self.vel_vector[0]

    # add the acceleration to the current velocity of the robot, up to the max-velocity -> positive velocity is a forward movement
    def move_forward(self):
        self.movement_direction()

    def draw(self, win, counter, robot, l_col, water_col):
        if l_col.col:
            win.blit(rot_center(explosion_effect[counter // 16], 0),
                     (robot.x - 14, robot.y - 10))  # draw the explosion animation

        win.blit(pygame.transform.rotate(self.robot_image, 0), (self.x, self.y))

        # draw a new surface of the robot under the water, it sould be drawn after the robot
        if water_col.col:   
            win.blit(water_col.under_water_surf, (self.x, self.y))

    def shoot(self, screen, v = 6, filename = "images/default_projectile.png", angle = None):
        if angle is None: angle = self.angle
        p = Projectile(self.x + 30, self.y + 30, angle, v, filename)  # FIXME projectile offset
        p.draw(screen)
        self.projectiles.append(p)
