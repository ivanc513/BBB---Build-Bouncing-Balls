import pygame
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
import random
from ui.widgets.button import Button
from tests.simulation import simulation_test
from core.objects.ball import Ball
from core.objects.ring import Ring
from core.world.world import World
from core.constraints.gravity import Gravity
from core.conditions.ball_count import BallCount

def pygame_display(width, height):
    return pygame.display.set_mode((width, height), 
        pygame.RESIZABLE)
    
def opengl_display(width, height):
    return pygame.display.set_mode((width, height),
        pygame.OPENGL | pygame.DOUBLEBUF)

def main_menu(SCREEN):
    pygame.display.set_caption("Menu")
    [width, height] = SCREEN
    screen = pygame_display(width, height)
    
    while True:

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        NEW_BUTTON = Button(image=None, pos=(width/2, 3 * height/10), 
            text_input="NEW SIMULATION", font = pygame.font.Font("ui/assets/OpenSans.ttf", 75), 
            base_color="#d7fcd4", hovering_color="White")
        LIBRARY_BUTTON = Button(image=None, pos=(width/2, 4.5 * height/10), 
            text_input="LIBRARY", font=pygame.font.Font("ui/assets/OpenSans.ttf", 75), 
            base_color="#d7fcd4", hovering_color="White")
        RECORDINGS_BUTTON = Button(image=None, pos=(width/2, 6 * height/10), 
            text_input="RECORDINGS", font=pygame.font.Font("ui/assets/OpenSans.ttf", 75), 
            base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=None, pos=(width/2, 7.5 * height/10), 
            text_input="QUIT", font=pygame.font.Font("ui/assets/OpenSans.ttf", 75), 
            base_color="#d7fcd4", hovering_color="White")

        MENU_TEXT = pygame.font.Font("ui/assets/OpenSans.ttf", 150).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(width/2, height/10))
                            
        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [NEW_BUTTON, LIBRARY_BUTTON, RECORDINGS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if NEW_BUTTON.checkForInput(MENU_MOUSE_POS):
                    return "SIMULATION"
                if LIBRARY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    return "LIBRARY"
                if RECORDINGS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    return "RECORDINGS"            
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    return "QUIT"

        pygame.display.update()

def library(SCREEN):
    return "MAIN_MENU"

def recordings(SCREEN):
    return "MAIN_MENU"
    
def simulation_window(SCREEN):

    WIDTH, HEIGHT = SCREEN

    # Initialize OpenGL display
    window = pygame.display.set_mode(
        (WIDTH, HEIGHT),
        pygame.OPENGL | pygame.DOUBLEBUF
    )
    pygame.display.set_caption("Simulation (OpenGL)")
    clock = pygame.time.Clock()

    # OpenGL perspective setup
    glViewport(0, 0, WIDTH, HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, WIDTH, HEIGHT, 0)  # top-left origin for 2D rendering
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Setup simulation world
    arena = Ring(
        center=(WIDTH / 2, HEIGHT / 2),
        radius=150,
        arc_degree=60,
        spinning_speed=0.01
    )

    world = World(
        arena,
        WIDTH,
        HEIGHT,
        constraints=[Gravity(10)],
        end_condition=BallCount(10)
    )

    # Spawn initial ball
    world.spawn(Ball(
        pos=[world.width / 2, world.height / 2 - 120],
        vel=[random.uniform(-4, 4), random.uniform(-1, 1)]
    ))

    running = True
    while running and world.running:
        dt = clock.tick(60) / 100.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # Update simulation logic
        world.update(dt)

        # --- OpenGL Rendering ---
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Draw world objects
        world.draw()  # You'll need a method that draws balls/arena using OpenGL

        pygame.display.flip()

    return "MAIN_MENU"

WINDOWS = {
    "MAIN_MENU" : main_menu,
    "LIBRARY" : library,
    "RECORDINGS" : recordings,
    "SIMULATION" : simulation_window,
    "QUIT" : lambda screen : "QUIT"
}
