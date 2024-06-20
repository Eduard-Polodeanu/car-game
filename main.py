import pygame

from computer_car import ComputerCar
from menu import Menu
from player_car import PlayerCar
from utils import draw_checkpoint_onclick, draw_rays

pygame.init()

WIN_SIZE = (1280, 720)
FPS = 60

surface_left_rays = pygame.Surface((WIN_SIZE[0], WIN_SIZE[1]), pygame.SRCALPHA)
surface_right_rays = pygame.Surface((WIN_SIZE[0], WIN_SIZE[1]), pygame.SRCALPHA)
surface_front_ray = pygame.Surface((WIN_SIZE[0], WIN_SIZE[1]), pygame.SRCALPHA)

LEVELS = [
    {
        "track_image": "assets/track-1.png",
        "track_border_image": "assets/track-1-hitbox.png",
        "checkpoints": [[(59, 163), (100, 204)], [(177, 130), (185, 190)], [(576, 130), (576, 191)], [(966, 132), (966, 188)], [(1033, 198), (1070, 148)], [(1067, 257), (1121, 231)], [(1177, 333), (1206, 282)], [(1201, 376), (1272, 376)], [(1177, 441), (1223, 477)], [(1089, 481), (1089, 538)], [(897, 483), (886, 539)], [(866, 463), (805, 485)], [(823, 406), (879, 430)], [(960, 357), (978, 412)], [(938, 311), (975, 266)], [(850, 223), (850, 277)], [(759, 261), (808, 295)], [(630, 452), (671, 496)], [(566, 448), (541, 497)], [(251, 261), (215, 307)], [(201, 315), (132, 301)], [(220, 413), (273, 384)], [(227, 447), (236, 508)], [(107, 418), (69, 461)], [(81, 378), (14, 385)]],
        "finish_line": [(11, 310), (76, 310)],
        "start_position": [(40, 340), (10, 340)]
    },
    {
        "track_image": "assets/track-2.png",
        "track_border_image": "assets/track-2-hitbox.png",
        "checkpoints": [[(428, 146), (369, 142)], [(369, 77), (431, 137)], [(443, 147), (499, 123)], [(449, 301), (511, 299)], [(525, 299), (571, 341)], [(586, 225), (621, 280)], [(857, 177), (885, 236)], [(976, 72), (982, 138)], [(996, 172), (1056, 165)], [(978, 267), (1027, 314)], [(953, 389), (889, 376)], [(910, 456), (975, 475)], [(830, 517), (876, 559)], [(775, 621), (824, 662)], [(613, 615), (558, 662)], [(546, 521), (597, 478)], [(512, 522), (458, 483)], [(442, 593), (471, 654)], [(426, 579), (369, 599)]],
        "finish_line": [(366, 474), (426, 477)],
        "start_position": [(390, 430), (360, 430)]
    },
    {
        "track_image": "assets/track-2.png",
        "track_border_image": "assets/track-2-hitbox.png",
        "checkpoints": [[(428, 146), (369, 142)], [(369, 77), (431, 137)], [(443, 147), (499, 123)], [(449, 301), (511, 299)], [(525, 299), (571, 341)], [(586, 225), (621, 280)], [(857, 177), (885, 236)], [(976, 72), (982, 138)], [(996, 172), (1056, 165)], [(978, 267), (1027, 314)], [(953, 389), (889, 376)], [(910, 456), (975, 475)], [(830, 517), (876, 559)], [(775, 621), (824, 662)], [(613, 615), (558, 662)], [(546, 521), (597, 478)], [(512, 522), (458, 483)], [(442, 593), (471, 654)], [(426, 579), (369, 599)]],
        "finish_line": [(366, 474), (426, 477)],
        "start_position": [(390, 430), (360, 430)]
    }
]


class GameEnvironment:
    def __init__(self, player_car, computer_car):
        self.window = pygame.display.set_mode(WIN_SIZE, flags=pygame.SCALED, vsync=1)
        self.clock = pygame.time.Clock()
        self.player_car = player_car
        self.computer_car = computer_car

        self.menu_booleans = {"show_menu": True, "is_game_paused": False, "show_nextlevel_menu": False, "show_endscreen": False, "is_perk_unlocked": True}
        self.menu = Menu(self.window, self.menu_booleans)
        
        self.is_game_over = False
        self.final_score = [0] * len(LEVELS)
        
        self.current_level = 0
        self.load_level(self.current_level)

        self.perks = [[0, 0, 0]]     # [engine upgrade, steering upgrade, enemy sabotage]
        
        self.new_checkpoint_pos = []


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

    def next_level(self, won_round):
        self.final_score[self.current_level] = self.player_car.current_score
        self.current_level += 1
        if self.current_level >= len(LEVELS):
            self.menu.menu_booleans["show_endscreen"] = True
            self.menu.end_screen(self.final_score)
            pygame.quit()
            quit()
        else:
            self.menu.menu_booleans["show_nextlevel_menu"] = True
            self.computer_car.car_level += 1
            
            self.perks.append(self.menu.next_level_menu(self.current_level, self.player_car.current_score, self.perks[len(self.perks)-1]))
            self.player_car.set_perks(self.perks[len(self.perks)-1])
            self.computer_car.set_perks(self.perks[len(self.perks)-1])
            self.load_level(self.current_level)

    def start(self):
        if self.menu.menu_booleans["show_menu"]:
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
                self.can_start_level = True
                if event.key == pygame.K_ESCAPE:
                    self.menu.menu_booleans["is_game_paused"] = True
                if event.key == pygame.K_m:
                    #self.is_show_menu = True
                    self.next_level(True)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = pygame.mouse.get_pos()
                self.new_checkpoint_pos.append(click_pos)
                self.new_checkpoint_pos, self.checkpoints = draw_checkpoint_onclick(self.new_checkpoint_pos, self.checkpoints)
            """"""
                
        if self.can_start_level:
            keys = pygame.key.get_pressed()
            self.move_player(keys)

            self.computer_car.move()
            self.computer_car.vel = 3

            if self.player_car.collide(self.track_border_mask) != None:
                self.player_car.hit_wall()


            surface_mask = pygame.mask.from_surface(surface_left_rays.convert_alpha())
            if surface_mask.overlap(self.track_border_mask, (0,0)):
                self.computer_car.angle += -self.computer_car.rotation_vel * 2
                
            surface_mask2 = pygame.mask.from_surface(surface_right_rays.convert_alpha())
            if surface_mask2.overlap(self.track_border_mask, (0,0)):
                self.computer_car.angle += self.computer_car.rotation_vel * 2

            surface_mask3 = pygame.mask.from_surface(surface_front_ray.convert_alpha())
            if surface_mask3.overlap(self.track_border_mask, (0,0)):
                self.computer_car.vel = self.computer_car.vel * 2/3


        self.draw()
        self.clock.tick(FPS)


    def draw(self):
        self.window.blit(self.track_border, (0, 0))
        
        surface_left_rays.fill((0,0,0,0))
        surface_right_rays.fill((0,0,0,0))
        surface_front_ray.fill((0,0,0,0))
        draw_rays(surface_left_rays, self.computer_car.center_pos, 105, self.computer_car.angle, 40) 
        draw_rays(surface_right_rays, self.computer_car.center_pos, 75, self.computer_car.angle, 40) 
        draw_rays(surface_front_ray, self.computer_car.center_pos, 90, self.computer_car.angle, 70) 
        self.window.blit(surface_left_rays, (0,0))
        self.window.blit(surface_right_rays, (0,0)) 
        self.window.blit(surface_front_ray, (0,0)) 

        self.window.blit(self.track, (0, 0))

        self.player_car.draw(self.window)
        self.computer_car.draw(self.window) 
        

        if not self.can_start_level:
            self.menu.draw_start_prompt()
            
        pygame.display.flip()


    def move_player(self, keys):
        is_moving = False

        if keys[pygame.K_a]:
            if not keys[pygame.K_s]:
                self.player_car.angle += self.player_car.rotation_vel
            else:
                self.player_car.angle -= self.player_car.rotation_vel
        if keys[pygame.K_d]:
            if not keys[pygame.K_s]:
                self.player_car.angle -= self.player_car.rotation_vel
            else:
                self.player_car.angle += self.player_car.rotation_vel
                
        if keys[pygame.K_w]:
            is_moving = True
            self.player_car.vel = min(self.player_car.vel + self.player_car.acceleration, self.player_car.max_vel)
            self.player_car.move()
        if keys[pygame.K_s]:
            is_moving = True
            self.player_car.vel = max(self.player_car.vel - self.player_car.acceleration, -self.player_car.max_vel/2)
            self.player_car.move()

        if not is_moving:
            self.player_car.vel = max(self.player_car.vel - self.player_car.acceleration/8, 0)
            self.player_car.move()




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
            game.next_level(won_round=True)
        elif game.computer_car.hit_finish():
            game.menu.menu_booleans["is_perk_unlocked"] = False
            game.next_level(won_round=False)
        
        if game.menu.menu_booleans["is_game_paused"] == True:
            print("GAME IS PAUSED")

        if game.is_game_over == True:
            running = False

    pygame.quit()