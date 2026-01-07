import pygame
import random
from core.world import World
from core.arena import Arena
from core.ball import Ball

pygame.init()

WIDTH, HEIGHT = 800, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

BLACK = (0, 0, 0)

arena = Arena(
    center=(WIDTH / 2, HEIGHT / 2),
    radius=150,
    arc_degree=60,
    spinning_speed=0.01
)

world = World(arena, WIDTH, HEIGHT, gravity=10)
world.spawn(Ball(
    pos=[world.width / 2, world.height / 2 - 120],
    vel=[random.uniform(-4, 4), random.uniform(-1, 1)]))

running = True
while running:
    dt = clock.tick(60) / 100.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    world.update(dt)

    window.fill(BLACK)
    world.draw(window)

    pygame.display.flip()

pygame.quit()

