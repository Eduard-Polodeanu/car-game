import pygame

from car import Car
from utils import is_point_on_line

ACCELERATION = 1


class PlayerCar(Car):
    def __init__(self):
        super().__init__()
        self.acceleration = ACCELERATION
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
            pygame.draw.line(window, "black", self.current_checkpoints[i][0], self.current_checkpoints[i][1], 3)
        pygame.draw.line(window, "white", self.finish_line_pos[0], self.finish_line_pos[1], 3)

    def move(self):
        super().move()
        self.hit_checkpoint()


    def move_input(self, keys):
        is_moving = False

        if keys[pygame.K_a]:
            if not keys[pygame.K_s]:    # if moving backwards, rotate the other direction
                self.angle += self.rotation_vel
            else:
                self.angle -= self.rotation_vel
        if keys[pygame.K_d]:
            if not keys[pygame.K_s]:
                self.angle -= self.rotation_vel
            else:
                self.angle += self.rotation_vel
                
        if keys[pygame.K_w]:
            is_moving = True
            self.vel = min(self.vel + self.acceleration, self.max_vel)
            self.move()
        if keys[pygame.K_s]:
            is_moving = True
            self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
            self.move()

        if not is_moving:
            self.vel = max(self.vel - self.acceleration/4, 0)
            self.move()

    def hit_wall(self):     # bounce the opposite way
        self.vel = -self.vel/3
        self.move()

    def hit_checkpoint(self):
        if len(self.current_checkpoints) > 0:
            if is_point_on_line(self.center_pos, self.current_checkpoints[0], max(self.img.get_width(), self.img.get_height())/2):
                self.current_score += round(100/len(self.original_checkpoints)*100)
                del self.current_checkpoints[0]
                self.checkpoints_left += -1

    def hit_finish(self):
        if self.checkpoints_left == 0 and is_point_on_line(self.center_pos, self.finish_line_pos, max(self.img.get_width(), self.img.get_height())/2):
            return True
        return False
    
    def set_perks(self, perks_list):
        if perks_list[0]:
            self.acceleration += 0.1
            self.max_vel += 0.5
        if perks_list[1]:
            self.rotation_vel += 1

