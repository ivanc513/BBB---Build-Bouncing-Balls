import pygame
from world import World
from arena import Arena

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

world = World(arena, WIDTH, HEIGHT, gravity=0.2)
world.spawn_ball([WIDTH / 2, HEIGHT / 2 - 120], [0, 0])

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    world.update()

    window.fill(BLACK)
    world.draw(window)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

