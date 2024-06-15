import pygame

from computer_car import ComputerCar
from player_car import PlayerCar
from utils import draw_checkpoint_onclick

pygame.init()

TRACK = pygame.image.load("assets/track2.png")
TRACK_BORDER = pygame.image.load("assets/track-hitbox2.png")
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

WIN_SIZE = (1280, 720)
FPS = 60

CHECKPOINTS = [[(738, 63), (712, 186)], [(848, 76), (799, 220)], [(968, 121), (870, 244)], [(903, 282), (1127, 272)], [(862, 347), (1033, 455)], [(762, 407), (818, 556)], [(631, 422), (624, 556)], [(503, 390), (421, 534)], [(419, 344), (234, 447)], [(392, 282), (147, 303)], [(451, 226), (262, 129)], [(525, 195), (452, 42)]]


class GameEnvironment:
    def __init__(self, player_car, computer_car):
        self.window = pygame.display.set_mode(WIN_SIZE, flags=pygame.SCALED, vsync=1)
        self.clock = pygame.time.Clock()
        self.player_car = player_car
        self.computer_car = computer_car
      
        self.checkpoints = CHECKPOINTS
        self.new_checkpoint_pos = []


    def play(self):
        is_game_over = False
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_game_over = True
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = pygame.mouse.get_pos()
                self.new_checkpoint_pos.append(click_pos)
                self.new_checkpoint_pos, self.checkpoints = draw_checkpoint_onclick(self.new_checkpoint_pos, self.checkpoints)

        keys = pygame.key.get_pressed()
        self.move_player(keys)

        self.computer_car.move()

        if self.player_car.collide(TRACK_BORDER_MASK) != None:
            self.player_car.hit_wall()


        self.draw()
        self.clock.tick(FPS)

        return is_game_over


    def draw(self):
        self.window.blit(TRACK, (0, 0))
        self.window.blit(TRACK_BORDER, (0, 0))

        self.player_car.draw(self.window)
        self.computer_car.draw(self.window)    
        
        pygame.display.flip()


    def move_player(self, keys):
        moving = False

        if keys[pygame.K_a]:
            if not keys[pygame.K_s]:
                self.player_car.rotate(left=True)
            else:
                self.player_car.rotate(right=True)
        if keys[pygame.K_d]:
            if not keys[pygame.K_s]:
                self.player_car.rotate(right=True)
            else:
                self.player_car.rotate(left=True)
        if keys[pygame.K_w]:
            moving = True
            self.player_car.move_forward()
        if keys[pygame.K_s]:
            moving = True
            self.player_car.move_backward()

        if not moving:
            self.player_car.reduce_speed()


if __name__ == '__main__':
    player_car = PlayerCar(CHECKPOINTS)
    computer_car = ComputerCar(CHECKPOINTS, car_level=2)
    game = GameEnvironment(player_car, computer_car)
    pygame.display.set_caption("Track navigator")

    running = True
    while running:
        is_game_over= game.play()
        if is_game_over == True:
            running = False

    pygame.quit()