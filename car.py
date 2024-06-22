import pygame
import math
from utils import blit_rotate_center, scale_image

CAR_IMG = scale_image(pygame.image.load("assets/car.png"), 0.5)
CAR_MASK = pygame.mask.from_surface(scale_image(pygame.image.load("assets/car-hitbox.png"), 0.5))
CAR_START_POS = (10, 340)

MAX_VELOCITY = 4
ROTATION_VELOCITY = 5
ACCELERATION = 1


class Car:
    def __init__(self, start_position=CAR_START_POS):
        self.img = CAR_IMG
        self.mask = CAR_MASK
        self.x, self.y = start_position
        self.center_pos = (self.x + self.img.get_width()/2, self.y + self.img.get_height()/2)
        self.angle = 0
        self.vel = 0
        self.max_vel = MAX_VELOCITY
        self.rotation_vel = ROTATION_VELOCITY
        self.acceleration = ACCELERATION
        
    def reset(self, checkpoints, finish_line_pos):
        self.angle = 0
        self.center_pos = (self.x + self.img.get_width()/2, self.y + self.img.get_height()/2)
        self.original_checkpoints = checkpoints[:]
        self.finish_line_pos = finish_line_pos[:]
     
    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move(self):
        self.angle = (self.angle + 360) % 360
        radians = math.radians(self.angle)
        self.y -= math.cos(radians) * self.vel
        self.x -= math.sin(radians) * self.vel
        self.center_pos = (self.x + self.img.get_width()/2, self.y + self.img.get_height()/2)


    def collide(self, mask, x=0, y=0):
        offset = (int(self.x - x), int(self.y - y))
        intersection_point = mask.overlap(self.mask, offset)
        return intersection_point

