import pygame

from car import Car
from utils import is_point_on_line


class PlayerCar(Car):
    def __init__(self, checkpoints):
        super().__init__(checkpoints)
        self.reset()

    def reset(self):
        self.vel = 0
        self.x, self.y = 250, 270
        self.reset_checkpoints()
        super().reset()

    def draw(self, window):
        super().draw(window)
        for i in range(0, len(self.checkpoints)):
            pygame.draw.line(window, (255, 0, 0), self.checkpoints[i][0], self.checkpoints[i][1], 3)
        pygame.draw.line(window, (0, 0, 255), self.finish_line_pos[0], self.finish_line_pos[1], 3)

    def move(self):
        super().move()
        self.hit_checkpoint()
        self.hit_finish()


    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration/2, 0)
        self.move()

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def reset_checkpoints(self):
        self.finish_line_pos = [(604, 49), (600, 185)]
        self.checkpoints = [[(738, 63), (712, 186)], [(848, 76), (799, 220)], [(968, 121), (870, 244)], [(903, 282), (1127, 272)], [(862, 347), (1033, 455)], [(762, 407), (818, 556)], [(631, 422), (624, 556)], [(503, 390), (421, 534)], [(419, 344), (234, 447)], [(392, 282), (147, 303)], [(451, 226), (262, 129)], [(525, 195), (452, 42)]]
        self.checkpoints_left = len(self.checkpoints)

    def hit_wall(self):
        self.vel = -self.vel/3
        self.move()

    def hit_checkpoint(self):
        if len(self.checkpoints):
            if is_point_on_line(self.center_pos, self.checkpoints[0], max(self.img.get_width(), self.img.get_height())/2):
                del self.checkpoints[0]
                self.checkpoints_left += -1

    def hit_finish(self):
        if is_point_on_line(self.center_pos, self.finish_line_pos, max(self.img.get_width(), self.img.get_height())/2) and self.checkpoints_left == 0:
            self.reset()


    