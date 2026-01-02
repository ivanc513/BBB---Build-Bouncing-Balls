import pygame
import numpy as np
import math

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

        if dist + ball.radius <= self.radius:
            return

        # Ball is touching boundary
        if ball.is_in and ball.__class__.is_in_arc(
            ball.pos, self.center, self.start_angle, self.end_angle
        ):
            ball.is_in = False
            return

        if ball.is_in:
            d_unit = d / dist
            ball.pos = self.center + (self.radius - ball.radius) * d_unit

            t = np.array([-d[1], d[0]])
            proj = (np.dot(ball.v, t) / np.dot(t, t)) * t
            ball.v = 2 * proj - ball.v
            ball.v += t * self.spinning_speed

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 165, 0),
                           self.center.astype(int), self.radius, 3)

        pygame.draw.arc(
            surface,
            (255, 255, 255),
            (
                self.center[0] - self.radius,
                self.center[1] - self.radius,
                self.radius * 2,
                self.radius * 2
            ),
            self.start_angle,
            self.end_angle,
            4
        )
