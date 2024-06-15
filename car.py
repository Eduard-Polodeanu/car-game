import pygame
import math
from utils import blit_rotate_center, calculate_angle, calculate_midpoint, get_random_point_on_line, scale_image

CAR_IMG = scale_image(pygame.image.load("assets/car.png"), 0.5)
CAR_MASK = pygame.mask.from_surface(scale_image(pygame.image.load("assets/car-hitbox.png"), 0.5))
CAR_START_POS = (250, 270)

MAX_VELOCITY = 3.5
ROTATION_VELOCITY = 4
ACCELERATION = 0.05

CHECKPOINTS = [[(738, 63), (712, 186)], [(848, 76), (799, 220)], [(968, 121), (870, 244)], [(903, 282), (1127, 272)], [(862, 347), (1033, 455)], [(762, 407), (818, 556)], [(631, 422), (624, 556)], [(503, 390), (421, 534)], [(419, 344), (234, 447)], [(392, 282), (147, 303)], [(451, 226), (262, 129)], [(525, 195), (452, 42)]]


class Car:
    def __init__(self, x=CAR_START_POS[0], y=CAR_START_POS[1]):
        self.img = CAR_IMG
        self.mask = CAR_MASK
        self.x, self.y = x, y
        self.center_pos = (self.x + self.img.get_width()/2, self.y + self.img.get_height()/2)
        self.angle = 0
        self.vel = 0
        self.max_vel = MAX_VELOCITY
        self.rotation_vel = ROTATION_VELOCITY
        self.acceleration = ACCELERATION
        self.checkpoints = CHECKPOINTS


    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel
        self.y -= vertical
        self.x -= horizontal
        self.center_pos = (self.x + self.img.get_width()/2, self.y + self.img.get_height()/2)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration/2, 0)
        self.move()

    def collide(self, mask, x=0, y=0):
        offset = (int(self.x - x), int(self.y - y))
        intersection_point = mask.overlap(self.mask, offset)
        return intersection_point





class PlayerCar(Car):
    def reset(self):
        self.x, self.y = CAR_START_POS
        self.angle = 0
        self.vel = 0
        self.center_pos = (self.x + self.img.get_width()/2, self.y + self.img.get_height()/2)

    def hit_wall(self):
        self.vel = -self.vel/3
        self.move()




class ComputerCar(Car):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.targets = []
        self.vel = 1


    def find_targets(self):
        for checkpoint in self.checkpoints:
            self.targets.append(get_random_point_on_line(checkpoint[0], checkpoint[1]))
        
    def update_angle(self):
        if len(self.targets) == 0:
            self.find_targets()
        
        target = self.targets[0]

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
        if car_rectangle.collidepoint(self.targets[0][0], self.targets[0][1]):
            del self.targets[0]

    def move(self):
        self.update_angle()
        self.reached_check()
        super().move()

    def draw_points(self, win):
        for target in self.targets:
            pygame.draw.circle(win, (255, 0, 0), target, 5)

    def draw(self, win):
        super().draw(win)
        self.draw_points(win)

    