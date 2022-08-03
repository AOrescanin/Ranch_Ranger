import pygame
import math
from settings import *

# ******************************************************************************************************************

class Bullet:
    def __init__(self, x, y, mouse_x, mouse_y, image):
        self.x = x
        self.y = y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.type = type
        self.angle = math.atan2(y-mouse_y, x-mouse_x)
        self.x_vel = math.cos(self.angle) * BULLET_SPEED
        self.y_vel = math.sin(self.angle) * BULLET_SPEED
        self.bullet_image = pygame.image.load(image).convert_alpha()

    # ******************************************************************************************************************

    def shoot(self, display):
        self.x -= int(self.x_vel)
        self.y -= int(self.y_vel)

        display.blit(self.bullet_image, (self.x, self.y))

    # ******************************************************************************************************************

    def off_screen(self):
        if not (-MAP_SIZE <= self.x <= MAP_SIZE) or not(-MAP_SIZE <= self.y <= MAP_SIZE):
            return True
