import math
import random
import pygame
import json
import os

LEADERBOARD_FILE = 'leaderboard.json'


def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)

def rotate_center_and_draw(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
    win.blit(rotated_image, new_rect.topleft)
    #win.blit(rotated_image, top_left)
    #pygame.draw.rect(win, (255, 0, 0), rotated_image.get_rect(topleft=top_left), 2)


def draw_checkpoint_onclick(checkpoint_pos, all_checkpoints):
    if len(checkpoint_pos) == 2:
        print("Checkpoint added: " + str(checkpoint_pos))
        all_checkpoints.append(checkpoint_pos)
        checkpoint_pos = []
        print("All checkpoints: ", all_checkpoints)
    return checkpoint_pos, all_checkpoints


def calculate_line_lenght(point1, point2):  # distanta euclidiana
    x1, y1 = point1
    x2, y2 = point2
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance

def is_point_on_line(point, line, tolerance):
    px, py = point
    (x1, y1), (x2, y2) = line   

    triangle_area_twice = abs((x2 - x1) * (y1 - py) - (x1 - px) * (y2 - y1))    # determinant
    line_length = calculate_line_lenght(line[0], line[1])

    if line_length != 0:
        dist = triangle_area_twice / line_length      # A = bh/2 => h = 2A/b
    else:
        dist = 0
    return dist <= tolerance

def calculate_angle(pos1, pos2):    # tg = op/ad
    x1, y1 = pos1
    x2, y2 = pos2
    delta_x = x2 - x1
    delta_y = y2 - y1

    if delta_y:
        angle = math.atan(delta_x / delta_y)
    else:
        angle = math.pi / 2
    return angle

def get_random_point_on_line(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    t = round(random.uniform(0.15, 0.85), 2)
    x_random = x1 + t * (x2 - x1)
    y_random = y1 + t * (y2 - y1)
    return (round(x_random), round(y_random))


def calculate_line_endpoints(start_x, start_y, angle, length):  # conv polar -> cartezian
    radians = math.radians(angle)
    end_x = start_x + length * math.cos(radians)
    end_y = start_y - length * math.sin(radians)
    return end_x, end_y

def draw_rays(surface, start_pos, direction, angle, length):
    surface.fill((0,0,0,0))
    end_x, end_y = calculate_line_endpoints(start_pos[0], start_pos[1], angle + direction, length)
    pygame.draw.line(surface, (0, 255, 0), start_pos, (end_x, end_y), 3)


def save_leaderboard(data):
        with open(LEADERBOARD_FILE, 'w') as f:
            json.dump(data, f)

def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:    # empty or corrupt
            return []
    else:
        return []
        
        