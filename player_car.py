import pygame

from car import Car
from utils import is_point_on_line


class PlayerCar(Car):
    def __init__(self, checkpoints):
        super().__init__(checkpoints)
        self.reset()
        self.acceleration = 0.2

    def reset(self):
        self.vel = 0
        self.x, self.y = 250, 270
        self.current_checkpoints = self.original_checkpoints[:]
        self.checkpoints_left = len(self.current_checkpoints)
        super().reset()

    def draw(self, window):
        super().draw(window)
        for i in range(0, len(self.current_checkpoints)):
            pygame.draw.line(window, (255, 0, 0), self.current_checkpoints[i][0], self.current_checkpoints[i][1], 3)
        pygame.draw.line(window, (0, 0, 255), self.finish_line_pos[0], self.finish_line_pos[1], 3)

    def move(self):
        super().move()
        self.hit_checkpoint()


    def hit_wall(self):
        self.vel = -self.vel/3
        self.move()

    def hit_checkpoint(self):
        if len(self.current_checkpoints):
            if is_point_on_line(self.center_pos, self.current_checkpoints[0], max(self.img.get_width(), self.img.get_height())/2):
                del self.current_checkpoints[0]
                self.checkpoints_left += -1

    def hit_finish(self):
        if is_point_on_line(self.center_pos, self.finish_line_pos, max(self.img.get_width(), self.img.get_height())/2) and self.checkpoints_left == 0:
            return True
        return False

    