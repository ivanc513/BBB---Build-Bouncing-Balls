import pygame
import os
from datetime import datetime
from copy import deepcopy
from OpenGL.GLU import *
from OpenGL.GL import *
from ui.widgets.button import Button
from tests.simulation import simulation_test
from core.objects.ball import Ball
from core.objects.ring import Ring
from core.world.world import World
from core.constraints.gravity import Gravity
from core.conditions.ball_count import BallCount
from library.sim_loader import load_simulation_from_json
from library.sim_file_handler import *

FONT_PATH = "ui/assets/OpenSans.ttf"

def pygame_display(width, height):
    return pygame.display.set_mode((width, height), 
        pygame.RESIZABLE)
    
def opengl_display(width, height):
    return pygame.display.set_mode((width, height),
        pygame.OPENGL | pygame.DOUBLEBUF)

def main_menu(SCREEN, state):
    pygame.display.set_caption("Menu")
    [width, height] = SCREEN
    screen = pygame_display(width, height)
    
    while True:

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        NEW_BUTTON = Button(image=None, pos=(width/2, 3 * height/10), 
            text_input="NEW SIMULATION", font = pygame.font.Font(FONT_PATH, 75), 
            base_color="#d7fcd4", hovering_color="White")
        LIBRARY_BUTTON = Button(image=None, pos=(width/2, 4.5 * height/10), 
            text_input="LIBRARY", font=pygame.font.Font(FONT_PATH, 75), 
            base_color="#d7fcd4", hovering_color="White")
        RECORDINGS_BUTTON = Button(image=None, pos=(width/2, 6 * height/10), 
            text_input="RECORDINGS", font=pygame.font.Font(FONT_PATH, 75), 
            base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=None, pos=(width/2, 7.5 * height/10), 
            text_input="QUIT", font=pygame.font.Font(FONT_PATH, 75), 
            base_color="#d7fcd4", hovering_color="White")

        MENU_TEXT = pygame.font.Font(FONT_PATH, 150).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(width/2, height/10))
                            
        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [NEW_BUTTON, LIBRARY_BUTTON, RECORDINGS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return {"next" : "QUIT"}
            if event.type == pygame.MOUSEBUTTONDOWN:
                if NEW_BUTTON.checkForInput(MENU_MOUSE_POS):
                    template_path = "library/simulation_template/default.json"

                    # Create a new file with timestamp
                    new_sim_path = create_new_sim_file(template_path)

                    # Load the world from the new file using your existing loader
                    world = load_simulation_from_json(new_sim_path, width, height)

                    return {
                        "next": "SIMULATION",
                        "world": world,
                    }
                if LIBRARY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    return {"next" : "LIBRARY"}
                if RECORDINGS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    return {"next" : "RECORDINGS"}          
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    return {"next" : "QUIT"}

        pygame.display.update()

def library(SCREEN, state):
    pygame.display.set_caption("Simulation Library")
    width, height = SCREEN
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    simulations = list_simulations()
    selected = None

    BACK_BUTTON = Button(
        image=None,
        pos=(width / 2, height * 0.9),
        text_input="BACK",
        font=pygame.font.Font(FONT_PATH, 60),
        base_color="#d7fcd4",
        hovering_color="White"
    )

    running = True
    while running:
        screen.fill((30, 30, 30))
        mouse_pos = pygame.mouse.get_pos()

        title = pygame.font.Font(FONT_PATH, 80).render("LIBRARY", True, "#b68f40")
        screen.blit(title, title.get_rect(center=(width/2, height*0.1)))

        y_offset = height * 0.2
        buttons = []

        for sim in simulations:
            btn = Button(
                image=None,
                pos=(width/2, y_offset),
                text_input=sim["name"],
                font=pygame.font.Font(FONT_PATH, 40),
                base_color="#AAAAAA",
                hovering_color="White"
            )
            btn.changeColor(mouse_pos)
            btn.update(screen)
            buttons.append((btn, sim))
            y_offset += 60

        BACK_BUTTON.changeColor(mouse_pos)
        BACK_BUTTON.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return {"next": "QUIT"}

            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(mouse_pos):
                    return {"next": "MAIN_MENU"}

                for btn, sim in buttons:
                    if btn.checkForInput(mouse_pos):
                        world = load_simulation_from_json(
                            f"library/simulations/{sim["filename"]}",
                            width,
                            height
                        )
                        return {
                            "next": "SIMULATION",
                            "world": world
                        }

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE and selected:
                    delete_simulation(selected)
                    simulations = list_simulations()
                    selected = None

        pygame.display.update()
        clock.tick(60)

def recordings(SCREEN, state):
    return "MAIN_MENU"
    
def simulation_window(SCREEN, state):

    WIDTH, HEIGHT = SCREEN

    # Initialize OpenGL display
    window = opengl_display(WIDTH, HEIGHT)
    pygame.display.set_caption("Simulation (OpenGL)")
    clock = pygame.time.Clock()
    world = state.get("world", state["world"])

    if world is None:
        print("ERROR: Entered SIMULATION with no world loaded")
        return {"next": "MAIN_MENU"}

    # OpenGL setup
    glViewport(0, 0, WIDTH, HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, WIDTH, HEIGHT, 0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    running = True
    while running and world.running:
        dt = clock.tick(60) / 100.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        world.update(dt)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        world.draw()

        pygame.display.flip()

    return {"next" : "MAIN_MENU"}

WINDOWS = {
    "MAIN_MENU" : main_menu,
    "LIBRARY" : library,
    "RECORDINGS" : recordings,
    "SIMULATION" : simulation_window,
    "QUIT" : lambda screen : "QUIT"
}
