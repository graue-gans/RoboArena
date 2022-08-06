
import pygame

from map_utility import Map

from robot import BossRobot, PatrolRobot, PlayerRobot, StaticRobot, Wall_Collision, Lava_Collision, Water_Collision
from upload_effects import player_robot_img, player_gun_img
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
        e1 = StaticRobot((810, 140), 180, image_robot, image_gun)
        return []

    def init_patrol_robots(self):
        p1 = PatrolRobot((810, 140), 180, 2, 2, 0.02, image_robot, image_gun, (0, 1000), (100, 500))
        return []

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
        bosses  = self.init_boss_robots()

        passed = False
        t1 = 0
        t2 = 0
        t3 = 0

        wall_col = Wall_Collision()
        lava_col = Lava_Collision()
        water_col = Water_Collision()

        while run:
            counter %= 60
            counter += 1

            self.close_event()
            self.render_background(self.screen)
            wall_col.wall_Robot_collision(self.wall_mask(), player)
            lava_col.lava_Robot_collision(self.lava_mask(), player)
            water_col.water_Robot_collision(self.water_mask(), player)
            player.move_robot(wall_col)
            player.draw(self.screen, counter, player, lava_col, water_col)  # FIXME player as argument??

            # static robots:
            for bot in statics:
                lava_col.lava_Robot_collision(self.lava_mask(), bot)
                water_col.water_Robot_collision(self.water_mask(), bot)
                if t1 > bot.firing_speed:
                    bot.act(self.screen)
                    passed = True
                bot.move_robot()  # FIXME
                bot.draw(self.screen, counter, bot, lava_col, water_col)  # FIXME
                bot.update_projectiles(self.screen)  # FIXME
            if passed:
                t1 = 0
                passed = False

            # patrol robots:
            for bot in patrols:
                lava_col.lava_Robot_collision(self.lava_mask(), bot)
                water_col.water_Robot_collision(self.water_mask(), bot)
                bot.act(self.screen, (player.x, player.y), t2 > 1500)
                bot.move_robot()  # FIXME
                bot.draw(self.screen, counter, bot, lava_col, water_col)  # FIXME
                bot.update_projectiles(self.screen)  # FIXME
            if t2 > 1500:
                t2 = 0

            # boss robots:
            for bot in bosses:
                lava_col.lava_Robot_collision(self.lava_mask(), bot)
                water_col.water_Robot_collision(self.water_mask(), bot)
                bot.act(self.screen, (player.x, player.y), flag=False, shooting=t3 > 1000)
                bot.move_robot()
                bot.draw(self.screen, counter, bot, lava_col, water_col)
                bot.update_projectiles(self.screen)
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

        pygame.quit()
