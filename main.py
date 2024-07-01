import pygame

from computer_car import ComputerCar
from menu import Menu
from player_car import PlayerCar
from utils import draw_checkpoint_onclick, draw_rays

pygame.init()

WIN_SIZE = (1280, 720)
FPS = 60

surface_left_rays = pygame.Surface(WIN_SIZE, pygame.SRCALPHA)
surface_right_rays = pygame.Surface(WIN_SIZE, pygame.SRCALPHA)
surface_front_ray = pygame.Surface(WIN_SIZE, pygame.SRCALPHA)

LEVELS = [
    {
        "track_image": "assets/track-1.png",
        "track_border_image": "assets/track-1-hitbox.png",
        "checkpoints": [[(172, 195), (109, 179)], [(234, 152), (201, 98)], [(378, 71), (353, 128)], [(444, 205), (496, 169)], [(636, 352), (616, 412)], [(807, 333), (852, 377)], [(1028, 290), (1021, 353)], [(1169, 425), (1243, 405)], [(1129, 519), (1169, 577)], [(991, 530), (1052, 586)], [(962, 597), (986, 657)], [(558, 599), (545, 669)], [(464, 546), (457, 612)], [(207, 524), (160, 582)], [(133, 475), (206, 463)], [(139, 381), (82, 413)]],
        "finish_line": [(74, 272), (140, 280)],
        "start_position": [(95, 337), (65, 337)],   # [player_pos, computer_pos]
        "ideal_time": 35,
        "max_time": 70
    },
    {
        "track_image": "assets/track-2.png",
        "track_border_image": "assets/track-2-hitbox.png",
        "checkpoints": [[(59, 163), (100, 204)], [(177, 130), (185, 190)], [(576, 130), (576, 191)], [(966, 132), (966, 188)], [(1033, 198), (1070, 148)], [(1067, 257), (1121, 231)], [(1177, 333), (1206, 282)], [(1201, 376), (1272, 376)], [(1177, 441), (1223, 477)], [(1089, 481), (1089, 538)], [(897, 483), (886, 539)], [(866, 463), (805, 485)], [(823, 406), (879, 430)], [(960, 357), (978, 412)], [(938, 311), (975, 266)], [(850, 223), (850, 277)], [(759, 261), (808, 295)], [(630, 452), (671, 496)], [(566, 448), (541, 497)], [(251, 261), (215, 307)], [(201, 315), (132, 301)], [(220, 413), (273, 384)], [(227, 447), (236, 508)], [(107, 418), (69, 461)], [(81, 378), (14, 385)]],
        "finish_line": [(11, 310), (76, 310)],
        "start_position": [(15, 340), (45, 340)],
        "ideal_time": 35,
        "max_time": 70
    },
    {
        "track_image": "assets/track-3.png",
        "track_border_image": "assets/track-3-hitbox.png",
        "checkpoints": [[(428, 146), (369, 142)], [(369, 77), (431, 137)], [(443, 147), (499, 123)], [(449, 301), (511, 299)], [(525, 299), (571, 341)], [(586, 225), (621, 280)], [(857, 177), (885, 236)], [(976, 72), (982, 138)], [(996, 172), (1056, 165)], [(978, 267), (1027, 314)], [(953, 389), (889, 376)], [(910, 456), (975, 475)], [(830, 517), (876, 559)], [(775, 621), (824, 662)], [(613, 615), (558, 662)], [(546, 521), (597, 478)], [(512, 522), (458, 483)], [(442, 593), (471, 654)], [(426, 579), (369, 599)]],
        "finish_line": [(366, 507), (427, 504)],
        "start_position": [(370, 430), (400, 430)],
        "ideal_time": 20,
        "max_time": 40
    }
]


class GameEnvironment:
    def __init__(self, player_car, computer_car):
        self.window = pygame.display.set_mode(WIN_SIZE, vsync=1)
        self.clock = pygame.time.Clock()
        self.player_car = player_car
        self.computer_car = computer_car

        self.menu_booleans = {"show_main_menu": True, "show_nextlevel_menu": False, "show_endscreen": False, "show_leaderboard_menu": False, "is_perk_unlocked": True}  # perk false
        self.menu = Menu(self.window, self.menu_booleans)
        
        self.is_game_over = False
        self.final_score = [0] * len(LEVELS)
        
        self.current_level = 0
        self.load_level(self.current_level)

        self.perks = [[0, 0, 0]]     # [engine upgrade, steering upgrade, enemy sabotage]
        
        self.new_checkpoint_pos = []    #


    def load_level(self, level_index):
        level_data = LEVELS[level_index]
        self.track = pygame.image.load(level_data["track_image"])
        self.track_border = pygame.image.load(level_data["track_border_image"])
        self.track_border_mask = pygame.mask.from_surface(self.track_border)
        self.checkpoints = level_data["checkpoints"]
        self.finish_line_pos = level_data["finish_line"]
        self.start_position = level_data["start_position"]
        self.player_car.reset(self.checkpoints, self.finish_line_pos, self.start_position[0])
        self.computer_car.reset(self.checkpoints, self.finish_line_pos, self.start_position[1])
        self.can_start_level = False

    def next_level(self):
        level_time = pygame.time.get_ticks() - self.start_time
        self.final_score[self.current_level] = self.calculate_score(level_time, self.current_level, self.player_car.current_score)
        self.current_level += 1
        if self.current_level >= len(LEVELS):
            self.menu.menu_booleans["show_endscreen"] = True
            self.menu.end_screen(self.final_score)
            self.reset_to_level_1()
        else:
            self.menu.menu_booleans["show_nextlevel_menu"] = True
            self.computer_car.car_level += 1
            
            self.perks.append(self.menu.next_level_menu(self.current_level, self.final_score[self.current_level-1], self.perks[len(self.perks)-1]))
            self.player_car.set_perks(self.perks[len(self.perks)-1])
            self.computer_car.set_perks(self.perks[len(self.perks)-1])

            self.load_level(self.current_level)

    def start(self):
        if self.menu.menu_booleans["show_main_menu"]:
            self.menu.main_menu()
        else:
            self.play()
            
    def play(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_game_over = True
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if self.can_start_level == False:
                    self.can_start_level = True
                    self.start_time = pygame.time.get_ticks()
                if event.key == pygame.K_m:
                    #self.is_show_menu = True
                    self.next_level()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = pygame.mouse.get_pos()
                self.new_checkpoint_pos.append(click_pos)
                self.new_checkpoint_pos, self.checkpoints = draw_checkpoint_onclick(self.new_checkpoint_pos, self.checkpoints)
            """"""
                
        if self.can_start_level:
            keys = pygame.key.get_pressed()
            self.player_car.move_input(keys)
            self.computer_car.move()

            if self.player_car.collide(self.track_border_mask) != None:
                self.player_car.hit_wall()


            surface_left_rays_mask = pygame.mask.from_surface(surface_left_rays.convert_alpha())
            if surface_left_rays_mask.overlap(self.track_border_mask, (0,0)):
                self.computer_car.angle += -self.computer_car.rotation_vel * 2
                pass
                
            surface_right_rays_mask = pygame.mask.from_surface(surface_right_rays.convert_alpha())
            if surface_right_rays_mask.overlap(self.track_border_mask, (0,0)):
                self.computer_car.angle += self.computer_car.rotation_vel * 2
                pass

            surface_front_ray_mask = pygame.mask.from_surface(surface_front_ray.convert_alpha())
            if surface_front_ray_mask.overlap(self.track_border_mask, (0,0)) and self.computer_car.vel > self.computer_car.max_vel / 2:
                self.computer_car.vel = self.computer_car.vel * 2/3
            else:
                self.computer_car.vel = self.computer_car.max_vel

        self.draw()
        self.clock.tick(FPS)


    def draw(self):
        self.window.blit(self.track_border, (0, 0))
        self.window.blit(self.track, (0, 0))

        for surface, direction, length in zip([surface_left_rays, surface_right_rays, surface_front_ray], [115, 65, 90], [40, 40, 75]):
            draw_rays(surface, self.computer_car.center_pos, direction, self.computer_car.angle, length) 
            self.window.blit(surface, (0,0))
        
        self.computer_car.draw(self.window)
        self.player_car.draw(self.window)
        
        if not self.can_start_level:
            self.menu.draw_start_prompt()
            
        pygame.display.update()


    def reset_to_level_1(self):
        self.current_level = 0
        self.load_level(self.current_level)
        self.perks = [[0, 0, 0]]
        self.computer_car.car_level = 1

    def calculate_score(self, level_time, level, checkpoints_score):
        ideal_time = LEVELS[level]["ideal_time"]
        max_time = LEVELS[level]["max_time"]
        level_time_seconds = level_time / 1000

        time_factor = max(0, 1 - (level_time_seconds - ideal_time) / (max_time - ideal_time))
        return round(checkpoints_score * time_factor)



if __name__ == '__main__':
    pygame.display.set_caption("Track navigator")
    
    player_car = PlayerCar()
    computer_car = ComputerCar(car_level=1)
    game = GameEnvironment(player_car, computer_car)

    running = True
    while running:
        game.start()

        if game.player_car.hit_finish():
            game.menu.menu_booleans["is_perk_unlocked"] = True
            game.next_level()
        elif game.computer_car.hit_finish():
            game.menu.menu_booleans["is_perk_unlocked"] = False
            game.next_level()

        if game.is_game_over == True:
            running = False

    pygame.quit()