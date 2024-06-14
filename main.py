import pygame

from car import Car
from utils import draw_checkpoint_onclick

pygame.init()

TRACK = pygame.image.load("assets/track2.png")
TRACK_BORDER = pygame.image.load("assets/track-hitbox2.png")
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

WIN_SIZE = (1280, 720)
FPS = 60

CHECKPOINTS = [[(738, 63), (712, 186)], [(848, 76), (799, 220)], [(968, 121), (870, 244)], [(903, 282), (1127, 272)], [(862, 347), (1033, 455)], [(762, 407), (818, 556)], [(631, 422), (624, 556)], [(503, 390), (421, 534)], [(419, 344), (234, 447)], [(392, 282), (147, 303)], [(451, 226), (262, 129)], [(525, 195), (452, 42)]]


class GameEnvironment:
    def __init__(self, car):
        self.window = pygame.display.set_mode(WIN_SIZE, flags=pygame.SCALED, vsync=1)
        self.clock = pygame.time.Clock()
        self.car = car
        self.reset()

    def reset(self):
        self.car.reset()
        self.score = 0
        self.reset_checkpoints()

    def reset_checkpoints(self):
        self.new_checkpoint_pos = []
        self.finish_line_pos = [(604, 49), (600, 185)]
        self.all_checkpoints = CHECKPOINTS

    def play(self):
        is_game_over = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_game_over = True
                pygame.quit()
                print('Final score: ', self.score)
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = pygame.mouse.get_pos()
                self.new_checkpoint_pos.append(click_pos)

        keys = pygame.key.get_pressed()
        self.move_player(keys)


        if self.car.collide(TRACK_BORDER_MASK) != None:
            self.car.hit_wall()


        self.draw()
        self.clock.tick(FPS)

        return is_game_over, self.score


    def draw(self):
        self.window.blit(TRACK, (0, 0))
        self.window.blit(TRACK_BORDER, (0, 0))

        self.car.draw(self.window)

        
        self.new_checkpoint_pos, self.all_checkpoints = draw_checkpoint_onclick(self.window, self.new_checkpoint_pos, self.all_checkpoints)        
        pygame.draw.line(self.window, (0, 0, 255), self.finish_line_pos[0], self.finish_line_pos[1], 3)
        
        pygame.display.flip()


    def move_player(self, keys):
        moving = False

        if keys[pygame.K_a]:
            if not keys[pygame.K_s]:
                self.car.rotate(left=True)
            else:
                self.car.rotate(right=True)
        if keys[pygame.K_d]:
            if not keys[pygame.K_s]:
                self.car.rotate(right=True)
            else:
                self.car.rotate(left=True)
        if keys[pygame.K_w]:
            moving = True
            self.car.move_forward()
        if keys[pygame.K_s]:
            moving = True
            self.car.move_backward()

        if not moving:
            self.car.reduce_speed()



if __name__ == '__main__':
    car = Car()
    game = GameEnvironment(car)
    pygame.display.set_caption("Track navigator")

    running = True
    while running:
        is_game_over, score = game.play()
        if is_game_over == True:
            running = False

    print('Final score: ', score)

    pygame.quit()