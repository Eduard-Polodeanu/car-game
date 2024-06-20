import pygame

from car import Car
from utils import is_point_on_line


class PlayerCar(Car):
    def __init__(self):
        super().__init__()
        self.current_score = 0

    def reset(self, checkpoints, finish_line_pos, start_position):
        super().reset(checkpoints, finish_line_pos)
        self.vel = 0
        self.x, self.y = start_position
        self.current_checkpoints = self.original_checkpoints[:]
        self.checkpoints_left = len(self.current_checkpoints)
        self.current_score = 0

    def draw(self, window):
        super().draw(window)
        for i in range(0, len(self.current_checkpoints)):
            pygame.draw.line(window, (0, 0, 0), self.current_checkpoints[i][0], self.current_checkpoints[i][1], 3)
        pygame.draw.line(window, (255, 255, 255), self.finish_line_pos[0], self.finish_line_pos[1], 3)

    def move(self):
        super().move()
        self.hit_checkpoint()


    def hit_wall(self):
        self.vel = -self.vel/3
        self.move()

    def hit_checkpoint(self):
        if len(self.current_checkpoints):
            if is_point_on_line(self.center_pos, self.current_checkpoints[0], max(self.img.get_width(), self.img.get_height())/2):
                self.current_score += round(100/len(self.original_checkpoints)*100)
                del self.current_checkpoints[0]
                self.checkpoints_left += -1

    def hit_finish(self):
        if is_point_on_line(self.center_pos, self.finish_line_pos, max(self.img.get_width(), self.img.get_height())/2) and self.checkpoints_left == 0:
            return True
        return False
    
    def set_perks(self, perks_list):
        if perks_list[0]:
            self.acceleration += 0.1
            self.max_vel += 0.5
            # print("Engine upgraded: ", self.acceleration, self.max_vel)
        if perks_list[1]:
            self.rotation_vel += 1
            # print("Steering upgraded: ", self.rotation_vel)

    