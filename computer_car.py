import pygame
import math

from car import Car
from utils import calculate_angle, get_random_point_on_line, is_point_on_line, scale_image

CAR_IMG = scale_image(pygame.image.load("assets/car-computer.png"), 0.5)
CAR_MASK = pygame.mask.from_surface(scale_image(pygame.image.load("assets/car-computer-hitbox.png"), 0.5))


class ComputerCar(Car):
    def __init__(self, car_level):
        super().__init__()
        self.img = CAR_IMG
        self.mask = CAR_MASK
        self.vel = self.max_vel
        self.car_level = car_level

    def reset(self, checkpoints, finish_line_pos, start_position):
        super().reset(checkpoints, finish_line_pos)
        self.x, self.y = start_position
        self.path_targets = []

    def draw(self, window):
        super().draw(window)
        for target in self.path_targets:
            pygame.draw.circle(window, "red", target, 8)
        
    def move(self):
        self.update_angle()
        self.hit_target()
        super().move()


    def find_targets(self):
        precision = 2 ** self.car_level
        for checkpoint in self.original_checkpoints + [self.finish_line_pos]:
            point_A, point_B = checkpoint
            delta_x = point_B[0] - point_A[0]
            delta_y = point_B[1] - point_A[1]

            x1 = point_A[0] + (0.5 + 1/precision) * delta_x
            y1 = point_A[1] + (0.5 + 1/precision) * delta_y
            point_M = (x1, y1)
            
            x2 = point_A[0] + (0.5 - 1/precision) * delta_x
            y2 = point_A[1] + (0.5 - 1/precision) * delta_y
            point_N = (x2, y2)

            target = get_random_point_on_line(point_M, point_N)
            self.path_targets.append(target)
        
    def update_angle(self):
        if len(self.path_targets) == 0:
            self.find_targets()
        else:
            target = self.path_targets[0]
            radian_angle = calculate_angle(self.center_pos, target)
            
            if target[1] > self.y:
                radian_angle += math.pi
            degrees_angle = math.degrees(radian_angle)
            difference_in_angle = self.angle - degrees_angle

            if difference_in_angle >= 180:
                difference_in_angle += -360
            if difference_in_angle <= -180:
                difference_in_angle += 360
            
            if difference_in_angle > 0:
                self.angle -= min(self.rotation_vel, abs(difference_in_angle))
            else:
                self.angle += min(self.rotation_vel, abs(difference_in_angle))

    def hit_target(self):
        car_rectangle = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        if car_rectangle.collidepoint(self.path_targets[0]):
            del self.path_targets[0]   

    def hit_finish(self):
        if len(self.path_targets) == 0 and is_point_on_line(self.center_pos, self.finish_line_pos, max(self.img.get_width(), self.img.get_height())/2):
            return True
        return False

    def set_perks(self, perks_list):
        if perks_list[2]:
            self.car_level += -1
            self.max_vel += -0.5

