import random
from ball import Ball

class World:
    def __init__(self, arena, width, height, gravity):
        self.arena = arena
        self.width = width
        self.height = height
        self.gravity = gravity
        self.balls = []

    def spawn_ball(self, pos, vel):
        self.balls.append(Ball(pos, vel))

    def update(self):
        new_balls = []

        for ball in self.balls:
            ball.update(self.gravity)
            self.arena.handle_collision(ball)

            # kill off-screen balls
            if (ball.pos[0] < 0 or ball.pos[0] > self.width or
                ball.pos[1] < 0 or ball.pos[1] > self.height):

                for _ in range(2):
                    new_balls.append(
                        Ball(
                            [self.width / 2, self.height / 2 - 120],
                            [random.uniform(-4, 4), random.uniform(-1, 1)]
                        )
                    )
            else:
                new_balls.append(ball)

        self.balls = new_balls
        self.arena.update()

    def draw(self, surface):
        self.arena.draw(surface)
        for ball in self.balls:
            ball.draw(surface)
