import math

import pygame

from movement_utility import rotate_at_center,rotate_at_pos

class Robot():
    """
    'Abstract' Robot class
    Contains the basic fields and methods for every robot
    """


    def __init__(self, start_position, max_velocity, rotation_velocity, acceleration,robot_image, robot_gun_image):
        self.x, self.y = start_position
        self.angle = 0
        self.weapon_angle = 0
        self.max_vel = max_velocity
        self.rotation_vel = rotation_velocity
        self.vel = 0
        self.a = acceleration
        self.vel_vector = [0, 0]
        self.robot_image = robot_image
        self.robot_gun_image = robot_gun_image
        self.colision = False



    #rotate the robot by adjusting the robot_angle
    def rotate_robot(self,left=False, right=False):
        if self.vel != 0:
            if left:
                self.angle += self.rotation_vel
            if right:
                self.angle -= self.rotation_vel

    #rotate the weapon by adjusting the weapon_angle
    def rotate_weapon(self, left=False, right=False):
        if left:
            self.weapon_angle += self.rotation_vel
        if right:
            self.weapon_angle -= self.rotation_vel

    #rotate the image of the robot and its weapon by using movement_utility.py functions
    def draw_robot(self,win):
        rotate_at_center(win, self.robot_image,(self.x,self.y),self.angle)
        #rotate_at_center(win, self.robot_gun_image,(self.x + 10,self.y + 5),self.weapon_angle) show the weapon
        pygame.display.update()

    #find the movement-direction for a given angle and move the robot
    def movement_direction(self):
        radians = math.radians(self.angle)
        self.vel_vector[0] = math.cos(radians) * self.vel
        self.vel_vector[1] = math.sin(radians) * self.vel
        self.y -= self.vel_vector[0]
        self.x -= self.vel_vector[1]
    #add the acceleration to the current velocity of the robot, up to the max-velocity -> positive velocity is a forward movement
    def move_forward(self):
        self.vel = min(self.vel + self.a, self.max_vel)
        self.movement_direction()
    #subtract the acceleration from the current velocity of the robot to -max_velocity -> negative velocity is a backward movement
    def move_backward(self):
        self.vel = max(self.vel - self.a, -self.max_vel / 2)
        self.movement_direction()

    #slow down the robot in forward movement with a given velocity
    def deceleration_forward(self,intensity):
        self.vel = max(self.vel - self.a * intensity, 0)
        self.movement_direction()

    #slow down the robot in backward movement with a given velocity
    def deceleration_backward(self,intensity):
        self.vel = min(self.vel + self.a * intensity, 0)
        self.movement_direction()
    #check if there is a collision
    def colision_check(self, mask1,img2, x=0, y=0):
        robo_mask = pygame.mask.from_surface(img2)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask1.overlap(robo_mask, offset)
        if poi is not None:
            return True
        else:
            return False
    #what todo if there is a collision with the lava
    def lava_collision(self):
        print("colision lava")

    #what todo if there is a collision with the wall
    def wall_collision(self):
        self.vel *= -1








# examplary classes that extend the 'abstract' Robot class
class BasicRobot(Robot):
    pass

class PlayerRobot(Robot):


      def move_robot(self):
          key = pygame.key.get_pressed()
          moving = False
          slowing_down_with_space = False #its True if the player presses 'space'


          if key[pygame.K_w] and key[pygame.K_s]:
              pass
          #using elif to not allow the player using 2-keys 'w' and 's'

          elif key[pygame.K_w]:
              moving = True
              self.move_forward()

          elif key[pygame.K_s]:
              moving = True
              self.move_backward()
        #------------------------------------------------------
         #slow down the robot with a higher intensity when the player presses 'space'
          if key[pygame.K_w] and key[pygame.K_SPACE] or key[pygame.K_s] and key[pygame.K_SPACE]:
              pass

          elif key[pygame.K_SPACE]:
              slowing_down_with_space = True
              if self.vel >= 0:
                  self.deceleration_forward(2) #2 is the decelereations intensity
              else:
                  self.deceleration_backward(2)


         #-----------------------------------------------
          #rotation of the robot and it's weapon
          if key[pygame.K_d]:
              self.rotate_robot(right=True)

          if key[pygame.K_a]:
              self.rotate_robot(left=True)

          if key[pygame.K_r]:
              self.rotate_weapon(right=True)
          if key[pygame.K_q]:
              self.rotate_weapon(left=True)

          #----------------------------------------------
          #slow down the robot when the player doesn't speed up up/backwards and when the player doesn't slow down with the 'space'-key

          if not moving and self.vel >= 0 and not slowing_down_with_space:
              self.deceleration_forward(1/2)

          if not moving and self.vel < 0 and not slowing_down_with_space:
              self.deceleration_backward(1/2)



class EnemyRobot(Robot):
    pass

