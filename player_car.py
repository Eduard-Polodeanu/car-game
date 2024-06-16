import pygame

from car import Car
from utils import is_point_on_line
LEFT_RAYS_DIRECTION = [120]
RIGHT_RAYS_DIRECTION = [60]

class PlayerCar(Car):
    def __init__(self, checkpoints):
        super().__init__(checkpoints)
        self.reset()
        self.left_rays_directions = LEFT_RAYS_DIRECTION
        self.right_rays_directions = RIGHT_RAYS_DIRECTION
        self.middle_line =  []
        self.abcd = []
        self.abcd2 = []

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
        # pygame.draw.line(window, (255, 255, 0), self.middle_line[0], self.middle_line[1], 3)

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
        self.checkpoints = [[(212, 217), (387, 260)], [(364, 114), (445, 208)], [(527, 75), (549, 174)], [(687, 72), (694, 163)], [(843, 98), (810, 191)], [(998, 170), (903, 252)], [(922, 306), (1083, 305)], [(884, 372), (977, 452)], [(750, 433), (779, 523)], [(597, 439), (585, 533)], [(465, 406), (425, 509)], [(386, 343), (242, 421)]]
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


    