import numpy as np
import pygame
import math
import random
from .base_object import SimObject

RED = (255, 0, 0)

class Ball(SimObject):
    def __init__(self, pos, vel, radius=5, color=RED, sfx=None):
        super().__init__(pos)
        self.v = np.array(vel, dtype=np.float64)
        self.radius = radius
        self.color = color
        self.sfx = sfx

        self.is_in = True

    @property
    def is_dynamic(self):
        return True

    def update(self, dt, world):
        self.pos += self.v * dt

    def draw(self, surface):
        pygame.draw.circle(
            surface, 
            self.color, 
            self.pos.astype(int), 
            self.radius
        )

    def on_collision(self, other, world):
        pass

    @staticmethod
    def is_in_arc(point, center, start_angle, end_angle):
        dx = point[0] - center[0]
        dy = point[1] - center[1]
        angle = math.atan2(dy, dx) % (2 * math.pi)
        start = start_angle % (2 * math.pi)
        end = end_angle % (2 * math.pi)

        if start <= end:
           return start <= angle <= end
        else:
        # Arc wraps past 0 radians
            return angle >= start or angle <= end
        
