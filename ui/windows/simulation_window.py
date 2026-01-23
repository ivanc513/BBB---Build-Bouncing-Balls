import pygame
import os
from recording.recording import ScreenRecorder
from OpenGL.GLU import *
from OpenGL.GL import *
from library.sim_file_handler import *

def opengl_display(width, height):
    return pygame.display.set_mode((width, height),
                                   pygame.OPENGL | pygame.DOUBLEBUF)

def simulation_window(SCREEN, state):
    WIDTH, HEIGHT = SCREEN

    # Screen recorder required even ints
    VIDEO_HEIGHT = int(HEIGHT) & ~1
    VIDEO_WIDTH = int(9 * (HEIGHT / 16)) & ~1

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

    recorder = None
    if getattr(world, "recording_enabled", False):
        os.makedirs("record/saved_videos", exist_ok=True)
        recorder = ScreenRecorder(
            output_path="saved_videos/simulation.mp4",
            width=VIDEO_WIDTH,
            height=VIDEO_HEIGHT,
            fps=60
        )
    if recorder:
        recorder.start()

    running = True
    while running and world.running:
        dt = clock.tick(60) / 100.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # Update simulation
        world.update(dt)

        # Clear screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Draw world
        world.draw()

        if recorder:
            pixels = glReadPixels(
                (WIDTH / 2) - (VIDEO_WIDTH / 2), 0, VIDEO_WIDTH, VIDEO_HEIGHT,
                GL_RGB,
                GL_UNSIGNED_BYTE
            )
            recorder.write_frame(pixels)

        pygame.display.flip()

    if recorder:
        recorder.stop()

    return {"next": "MAIN_MENU"}

