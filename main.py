import pygame

from button import Button
from computer_car import ComputerCar
from player_car import PlayerCar
from utils import draw_checkpoint_onclick, draw_rays

pygame.init()

WIN_SIZE = (1280, 720)
FPS = 60

BG_IMG = pygame.image.load("assets/menu-bg.png")
BUTTON_IMG = pygame.image.load("assets/button.png")
FONT_100 = pygame.font.SysFont("arialblack", 100)
FONT_60 = pygame.font.SysFont("arialblack", 60)

surface_left_rays = pygame.Surface((WIN_SIZE[0], WIN_SIZE[1]), pygame.SRCALPHA)
surface_right_rays = pygame.Surface((WIN_SIZE[0], WIN_SIZE[1]), pygame.SRCALPHA)



LEVELS = [
    {
        "track_image": "assets/track-1.png",
        "track_border_image": "assets/track-1-hitbox.png",
        "checkpoints": [[(59, 163), (100, 204)], [(177, 130), (185, 190)], [(576, 130), (576, 191)], [(966, 132), (966, 188)], [(1033, 198), (1070, 148)], [(1067, 257), (1121, 231)], [(1177, 333), (1206, 282)], [(1201, 376), (1272, 376)], [(1177, 441), (1223, 477)], [(1089, 481), (1089, 538)], [(897, 483), (886, 539)], [(866, 463), (805, 485)], [(823, 406), (879, 430)], [(960, 357), (978, 412)], [(968, 343), (1066, 356)], [(938, 311), (975, 266)], [(850, 223), (850, 277)], [(759, 261), (808, 295)], [(630, 452), (671, 496)], [(566, 448), (541, 497)], [(251, 261), (215, 307)], [(201, 315), (132, 301)], [(220, 413), (273, 384)], [(228, 449), (270, 499)], [(107, 418), (69, 461)], [(81, 378), (14, 385)]],
        "finish_line": [(11, 310), (76, 310)],
        "start_position": [(40, 340), (10, 340)]
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
        pygame.display.set_caption("Track navigator")
        self.clock = pygame.time.Clock()
        self.player_car = player_car
        self.computer_car = computer_car

        self.is_show_menu = True
        self.is_game_over = False
        self.is_game_paused = False

        self.current_level = 0
        self.load_level(self.current_level)

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

    def next_level(self):
        self.current_level += 1
        if self.current_level >= len(LEVELS):
            print("You have completed all levels!")
            pygame.quit()
            quit()
        else:
            self.computer_car.car_level += 1
            self.load_level(self.current_level)

    def start(self):
        if self.is_show_menu:
            self.main_menu()
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
                    self.is_game_paused = True
                if event.key == pygame.K_m:
                    self.is_show_menu = True
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = pygame.mouse.get_pos()
                self.new_checkpoint_pos.append(click_pos)
                self.new_checkpoint_pos, self.checkpoints = draw_checkpoint_onclick(self.new_checkpoint_pos, self.checkpoints)
            """"""
                
        if self.can_start_level:
            keys = pygame.key.get_pressed()
            self.move_player(keys)

            self.computer_car.move()

            if self.player_car.collide(self.track_border_mask) != None:
                self.player_car.hit_wall()


            surface_mask = pygame.mask.from_surface(surface_left_rays.convert_alpha())
            if surface_mask.overlap(self.track_border_mask, (0,0)):
                self.computer_car.angle += -self.computer_car.rotation_vel * 2
                
            surface_mask = pygame.mask.from_surface(surface_right_rays.convert_alpha())
            if surface_mask.overlap(self.track_border_mask, (0,0)):
                self.computer_car.angle += self.computer_car.rotation_vel * 2

        else:
            pass
            #print("wait for input")



        self.draw()
        self.clock.tick(FPS)


    def draw(self):
        self.window.blit(self.track_border, (0, 0))
        
        surface_left_rays.fill((0,0,0,0))
        surface_right_rays.fill((0,0,0,0))
        draw_rays(surface_left_rays, self.computer_car.center_pos, 105, self.computer_car.angle, 40) 
        draw_rays(surface_right_rays, self.computer_car.center_pos, 75, self.computer_car.angle, 40) 
        self.window.blit(surface_left_rays, (0,0))
        self.window.blit(surface_right_rays, (0,0)) 
        self.window.blit(self.track, (0, 0))

        self.player_car.draw(self.window)
        self.computer_car.draw(self.window) 
        
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


    def main_menu(self):
        while self.is_show_menu:
            self.window.blit(BG_IMG, (0, 0))
            #self.window.fill("#726E6E")

            mouse_pos = pygame.mouse.get_pos()

            MENU_TEXT = FONT_100.render("MAIN MENU", True, "#f1f4c6")
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

            PLAY_BUTTON = Button(BUTTON_IMG, (640, 320), "START", FONT_60, "#f1f4c6", "white")
            OPTIONS_BUTTON = Button(BUTTON_IMG, (640, 450), "OPTIONS", FONT_60, "#f1f4c6", "white")
            QUIT_BUTTON = Button(BUTTON_IMG, (640, 580), "QUIT", FONT_60, "#f1f4c6", "white")

            self.window.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.changeColor(mouse_pos)
                button.update(self.window)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(mouse_pos):
                        self.is_show_menu = False
                    if OPTIONS_BUTTON.checkForInput(mouse_pos):
                        pass
                    if QUIT_BUTTON.checkForInput(mouse_pos):
                        pygame.quit()
                        quit()

            pygame.display.flip()





if __name__ == '__main__':
    player_car = PlayerCar()
    computer_car = ComputerCar(car_level=1)
    game = GameEnvironment(player_car, computer_car)

    running = True
    while running:
        game.start()

        if game.player_car.hit_finish() or game.computer_car.hit_finish():
            game.next_level()
        
        if game.is_game_paused == True:
            print("GAME IS PAUSED")

        if game.is_game_over == True:
            running = False

    pygame.quit()