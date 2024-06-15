import pygame

from car import ComputerCar, PlayerCar
from utils import draw_checkpoint_onclick

pygame.init()

TRACK = pygame.image.load("assets/track2.png")
TRACK_BORDER = pygame.image.load("assets/track-hitbox2.png")
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

WIN_SIZE = (1280, 720)
FPS = 60


class GameEnvironment:
    def __init__(self, player_car, computer_car):
        self.window = pygame.display.set_mode(WIN_SIZE, flags=pygame.SCALED, vsync=1)
        self.clock = pygame.time.Clock()
        self.player_car = player_car
        self.computer_car = computer_car
        self.reset()

    def reset(self):
        self.player_car.reset()
        self.score = 0
        self.reset_checkpoints()

    def reset_checkpoints(self):
        self.new_checkpoint_pos = []
        self.finish_line_pos = [(604, 49), (600, 185)]
        self.all_checkpoints = self.player_car.checkpoints

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

        keys = pygame.key.get_pressed()
        self.move_player(keys)

        self.computer_car.move()


        if self.player_car.collide(TRACK_BORDER_MASK) != None:
            self.player_car.hit_wall()


        self.draw()
        self.clock.tick(FPS)

        return is_game_over, self.score


    def draw(self):
        self.window.blit(TRACK, (0, 0))
        self.window.blit(TRACK_BORDER, (0, 0))

        self.player_car.draw(self.window)
        self.computer_car.draw(self.window)

        
        self.new_checkpoint_pos, self.all_checkpoints = draw_checkpoint_onclick(self.window, self.new_checkpoint_pos, self.all_checkpoints)        
        pygame.draw.line(self.window, (0, 0, 255), self.finish_line_pos[0], self.finish_line_pos[1], 3)
        
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
    player_car = PlayerCar()
    computer_car = ComputerCar(275, 270)
    game = GameEnvironment(player_car, computer_car)
    pygame.display.set_caption("Track navigator")

    running = True
    while running:
        is_game_over, score = game.play()
        if is_game_over == True:
            running = False

    pygame.quit()