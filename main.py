import pygame

pygame.init()
WIDTH = 800
HEIGHT = 800
window = pygame.display.setmode((WIDTH, HEIGHT)) # We can set flags to further modify window
clock = pygame.time.Clock()
BLACK = (0, 0, 0)
running = True

# Main event loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    window.fill(BLACK)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()