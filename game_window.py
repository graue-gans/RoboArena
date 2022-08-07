import sys

import pygame

from Game_Info import *
from map_utility import Map

from robot import BossRobot, PatrolRobot, PlayerRobot, StaticRobot, Wall_Collision, Lava_Collision, Water_Collision, \
    Robot_Projectile_Collision
from upload_effects import *
from weather import Rain, Snow

# for debugging
image_robot = pygame.image.load("images/boss.png")
image_gun = pygame.image.load("images/Gun_01.png")


# end debugging


class Game_window(Map):
    image_robot_player = player_robot_img
    image_gun_player = player_gun_img

    file = 'maps/background.csv'
    pygame.init()

    def __init__(self, weather):
        super().__init__()
        self.load_background(self.main_map)
        self.weather = weather
        self.game()

    def init_static_robots(self):
        e1 = StaticRobot((40, 810), 0, enemy_static_image, enemy_static_gun)
        return [e1]

    def init_patrol_robots(self):
        p1 = PatrolRobot((910, 810), 0, 2, 2, 0.02, enemy_patrol_image, enemy_patrol_gun, (0, 1000), (400, 900))
        return [p1]

    def init_boss_robots(self):
        b1 = BossRobot((810, 180), 180, 2, 0.02, image_robot, self.background, (200, 200))
        return [b1]

    # the game loop
    def game(self):
        run = True

        player = PlayerRobot((200, 200), 2, 2, 0.02, player_robot_img, player_gun_img)  # create a player_robot
        counter = 0
        rain = [Rain() for i in range(300)]
        snow = [Snow() for i in range(300)]

        statics = self.init_static_robots()
        patrols = self.init_patrol_robots()
        bosses = self.init_boss_robots()

        passed = False
        t1 = 0
        t2 = 0
        t3 = 0


        wall_col = Wall_Collision()
        lava_col = Lava_Collision()
        water_col = Water_Collision()

        p_col = Robot_Projectile_Collision()

        while run:
            self.close_event()
            counter %= 60
            counter += 1
            key = pygame.key.get_pressed()
            if key[pygame.K_p]:  # pausing the game by pressing p
                self.pausing()

            if key[pygame.K_ESCAPE]:  # back to the manu by pressing Escape
                run = False

            self.render_background(self.screen)
            show_life_player(player_life_image, self.screen, player)

            show_life_enemy(enemy_life_image, self.screen, statics)
            show_life_enemy(enemy_life_image, self.screen, patrols)
            show_life_enemy(enemy_life_image, self.screen, bosses)

            self.kill_enemy(statics)
            self.kill_enemy(patrols)
            self.kill_enemy(bosses)
            self.game_Lost(player,"Game_Over, You Lost  "
                                            "Press Espace to quite the game")
            self.game_Won(bosses, "Game_Over You Won  "
                                  "Press Espace to quite the game")

            wall_col.wall_Player_Robot_collision(self.wall_mask(), player)
            lava_col.lava_Robot_collision(self.lava_mask(), player)
            water_col.water_Robot_collision(self.water_mask(), player)
            player.move_robot(wall_col)

            if key[pygame.K_f]:  # shoot with f
                player.shoot(self.screen)

            player.update_projectiles(self.screen)
            player.draw(self.screen, counter, lava_col, water_col)

            # static robots:

            for bot in statics:
                wall_col.wall_bot_collision(self.wall_mask(), bot)
                lava_col.lava_Robot_collision(self.lava_mask(), bot)
                water_col.water_Robot_collision(self.water_mask(), bot)
                if t1 > bot.firing_speed:
                    bot.act(self.screen)
                    passed = True
                bot.move_robot()  # FIXME
                bot.draw(self.screen, counter, lava_col, water_col)
                bot.update_projectiles(self.screen)  # FIXME

                p_col.get_hit(bot, player, 1)  # enemy hits the player
                p_col.get_hit(player, bot, 1)  # player hits the enemy

                for p in bot.projectiles:
                    if wall_col.wall_projectile_collision(self.wall_mask(), p):
                        bot.projectiles.remove(p)
            if passed:
                t1 = 0
                passed = False

            # patrol robots:
            for bot in patrols:
                wall_col.wall_bot_collision(self.wall_mask(), bot)
                lava_col.lava_Robot_collision(self.lava_mask(), bot)
                water_col.water_Robot_collision(self.water_mask(), bot)
                bot.act(self.screen, (player.x, player.y), t2 > 1500)
                bot.move_robot()  # FIXME
                bot.draw(self.screen, counter, lava_col, water_col)  # FIXME
                bot.update_projectiles(self.screen)  # FIXME

                p_col.get_hit(bot, player, 1)  # enemy hits robot
                p_col.get_hit(player, bot, 1)  # player hits the enemy

                for p in bot.projectiles:
                    if wall_col.wall_projectile_collision(self.wall_mask(), p):
                        bot.projectiles.remove(p)
            if t2 > 1500:
                t2 = 0

            # boss robots:
            for bot in bosses:
                wall_col.wall_bot_collision(self.wall_mask(), bot)
                lava_col.lava_Robot_collision(self.lava_mask(), bot)
                water_col.water_Robot_collision(self.water_mask(), bot)
                bot.act(self.screen, (player.x, player.y), flag=False, shooting=t3 > 1000)
                bot.move_robot()
                bot.draw(self.screen, counter, lava_col, water_col)
                bot.update_projectiles(self.screen)

                p_col.get_hit(bot, player, 2)  # enemy hits robot
                p_col.get_hit(player, bot, 1)  # player hits the enemy

                for p in bot.projectiles:
                    if wall_col.wall_projectile_collision(self.wall_mask(), p):
                        bot.projectiles.remove(p)

            if t3 > 1000:
                t3 = 0

            if self.weather == "rain":
                for i in range(Rain.start_rain(len(rain))):
                    rain[i].show()
                    rain[i].update()
            if self.weather == "snow":
                for i in range(Snow.start_snow(len(snow))):
                    snow[i].show()
                    snow[i].update()

            dt = self.update_screen()
            t1 += dt
            t2 += dt
            t3 += dt
    #pause the game
    def pausing(self):
        run = True
        while run:
            self.close_event()
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] or key[pygame.K_ESCAPE]:  # press space to unpause and Escape to go to the manu
                run = False
            pausing_info(self.screen, font1, "press p to pause, space to unpause  "
                                             "and press escape to go back to the menu", (255, 255, 255))

            pygame.display.flip()

    #shows a new game lost window
    def game_Lost(self,robot,massage):
        run = True
        if robot.life == 0:
            while run:
                self.close_event()
                key = pygame.key.get_pressed()
                if key[pygame.K_ESCAPE]: # Escape to go to the manu
                    run = False
                pausing_info(self.screen, font1,massage, (255, 255, 255))
                pygame.display.flip()
    #shows a new game won window
    def game_Won(self, robot, massage):
        run = True
        if len(robot) != 0:
            if robot[0].life == 1:
                while run:
                    self.close_event()
                    key = pygame.key.get_pressed()
                    if key[pygame.K_ESCAPE]:  # Escape to go to the manu
                        run = False
                    pausing_info(self.screen, font1, massage, (255, 255, 255))
                    pygame.display.flip()


    #removs the enemy from the map
    def kill_enemy(self,robot):
        if len(robot) != 0:
            if robot[0].life == 0:
                for r in robot:
                    robot.remove(r)







