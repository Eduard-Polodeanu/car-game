import pygame
import math
from utils import blit_rotate_center, calculate_angle, get_random_point_on_line, is_point_on_line, scale_image

CAR_IMG = scale_image(pygame.image.load("assets/car.png"), 0.5)
CAR_MASK = pygame.mask.from_surface(scale_image(pygame.image.load("assets/car-hitbox.png"), 0.5))
CAR_START_POS = (250, 270)

MAX_VELOCITY = 3.5
ROTATION_VELOCITY = 4
ACCELERATION = 0.05


class Car:
    def __init__(self, checkpoints, x=CAR_START_POS[0], y=CAR_START_POS[1]):
        self.img = CAR_IMG
        self.mask = CAR_MASK
        self.x, self.y = x, y
        self.center_pos = (self.x + self.img.get_width()/2, self.y + self.img.get_height()/2)
        self.angle = 0
        self.vel = 0
        self.max_vel = MAX_VELOCITY
        self.rotation_vel = ROTATION_VELOCITY
        self.acceleration = ACCELERATION
        self.checkpoints = checkpoints
        
    def reset(self):
        self.angle = 0
        self.center_pos = (self.x + self.img.get_width()/2, self.y + self.img.get_height()/2)
     
    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move(self):
        self.angle = (self.angle + 360) % 360
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel
        self.y -= vertical
        self.x -= horizontal
        self.center_pos = (self.x + self.img.get_width()/2, self.y + self.img.get_height()/2)


    def collide(self, mask, x=0, y=0):
        offset = (int(self.x - x), int(self.y - y))
        intersection_point = mask.overlap(self.mask, offset)
        return intersection_point




