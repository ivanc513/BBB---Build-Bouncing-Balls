import pygame
import numpy as np
import math
from core.objects.ball import Ball
from .base_object import SimObject

class Arena(SimObject):
    def __init__(self, center, radius, arc_degree, spinning_speed):
        super().__init__(center)
        self.radius = radius
        self.spinning_speed = spinning_speed

        arc_rad = math.radians(arc_degree)
        self.start_angle = -arc_rad / 2
        self.end_angle = arc_rad / 2

    @property
    def is_dynamic(self):
        return False  # the arena itself doesn't move position

    def update(self, dt, world):
        self.start_angle += self.spinning_speed * dt * 5
        self.end_angle += self.spinning_speed * dt * 5

    def on_collision(self, other, world):
        # Only handle dynamic objects like balls
        if not getattr(other, "is_dynamic", False):
            return

        d = other.pos - self.pos
        dist = np.linalg.norm(d)

        if dist < self.radius - other.radius:
            return

        # Object leaves arc
        if getattr(other, "is_in") and Ball.is_in_arc(other.pos, self.pos, self.start_angle, self.end_angle):
            if np.dot(other.v, d) > 0:   # moving outward
                other.is_in = False
                return

        if getattr(other, "is_in"):
            n = d / dist
            other.pos = self.pos + (self.radius - other.radius) * n

            n = d / dist                # unit normal
            other.pos = self.pos + n * (self.radius - other.radius)

            vn = np.dot(other.v, n)
            other.v = other.v - 2 * vn * n
            t = np.array([-n[1], n[0]])     # unit tangent
            other.v += t * self.spinning_speed * self.radius

            if (getattr(other, "sfx", None) != None):
                other.sfx.play() # User may add custom sfx


    def draw(self, surface):
        pygame.draw.circle(surface, (255, 165, 0),
                           self.pos.astype(int), self.radius, 3) 
        # Circle arc
        p1 = self.pos + (self.radius+1000) * np.array([math.cos(self.start_angle), math.sin(self.start_angle)])
        p2 = self.pos + (self.radius+1000) * np.array([math.cos(self.end_angle), math.sin(self.end_angle)])
        pygame.draw.polygon(surface, (0, 0, 0), [self.pos,p1,p2], 0)
