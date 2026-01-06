import pygame
import numpy as np
import math
from ball import Ball

class Arena:
    def __init__(self, center, radius, arc_degree, spinning_speed):
        self.center = np.array(center, dtype=np.float64)
        self.radius = radius
        self.spinning_speed = spinning_speed

        arc_rad = math.radians(arc_degree)

        self.start_angle = -arc_rad / 2
        self.end_angle = arc_rad / 2

    def update(self):
        self.start_angle += self.spinning_speed
        self.end_angle += self.spinning_speed

    def handle_collision(self, ball):
        d = ball.pos - self.center
        dist = np.linalg.norm(d)

        if dist < self.radius - ball.radius:
            return

        if ball.is_in and Ball.is_in_arc(ball.pos, self.center,
                                self.start_angle, self.end_angle):
            if np.dot(ball.v, d) > 0:   # moving outward
                ball.is_in = False
                return

        if ball.is_in:
            d_unit = d / dist
            ball.pos = self.center + (self.radius - ball.radius) * d_unit

            n = d / dist                # unit normal
            ball.pos = self.center + n * (self.radius - ball.radius)

            vn = np.dot(ball.v, n)
            ball.v = ball.v - 2 * vn * n
            t = np.array([-n[1], n[0]])     # unit tangent
            ball.v += t * self.spinning_speed * self.radius

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 165, 0),
                           self.center.astype(int), self.radius, 3) 
        # Circle arc
        p1 = self.center + (self.radius+1000) * np.array([math.cos(self.start_angle), math.sin(self.start_angle)])
        p2 = self.center + (self.radius+1000) * np.array([math.cos(self.end_angle), math.sin(self.end_angle)])
        pygame.draw.polygon(surface, (0, 0, 0), [self.center,p1,p2], 0)
