import pygame
import math

from car import Car
from utils import calculate_angle, get_random_point_on_line


LEFT_RAYS_DIRECTION = [150, 120]
RIGHT_RAYS_DIRECTION = [30, 60]

class ComputerCar(Car):
    def __init__(self, checkpoints, car_level):
        super().__init__(checkpoints)
        self.reset()
        self.path_targets = []
        self.vel = 2
        self.car_level = car_level
        self.left_rays_directions = LEFT_RAYS_DIRECTION
        self.right_rays_directions = RIGHT_RAYS_DIRECTION

    def reset(self):
        self.x, self.y = 275, 270
        super().reset()

    def draw(self, window):
        super().draw(window)
        for target in self.path_targets:
            pygame.draw.circle(window, (255, 0, 0), target, 5)
        
    def move(self):
        self.update_angle()
        self.reached_check()
        super().move()


    def find_targets(self):
        precision = 2 ** self.car_level
        for checkpoint in self.checkpoints:
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
        
        target = self.path_targets[0]

        radian_angle = calculate_angle((self.x, self.y), target)

        if target[1] > self.y:
            radian_angle += math.pi
        degrees_angle = math.degrees(radian_angle)
        difference_in_angle = self.angle - degrees_angle

        if difference_in_angle >= 180:
            difference_in_angle -= 360

        if difference_in_angle > 0:
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))
        else:
            self.angle += min(self.rotation_vel, abs(difference_in_angle))


    def reached_check(self):
        car_rectangle = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        if car_rectangle.collidepoint(self.path_targets[0]):
            del self.path_targets[0]

    
