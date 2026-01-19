import pygame
from OpenGL.GLU import *
from OpenGL.GL import *
from ui.widgets.button import Button
from ui.widgets.dropdown import Dropdown

FONT_PATH = "ui/assets/OpenSans.ttf"

ui_commands = []

def queue_object(obj_type):
    ui_commands.append(("ADD_OBJECT", obj_type))

def queue_constraint(c_type):
    ui_commands.append(("ADD_CONSTRAINT", c_type))

def queue_condition(cond_type):
    ui_commands.append(("ADD_CONDITION", cond_type))

def opengl_display(width, height):
    return pygame.display.set_mode((width, height),
                                   pygame.OPENGL | pygame.DOUBLEBUF)

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

    # Apply queued UI commands to world
    for cmd, arg in ui_commands:
        if cmd == "ADD_OBJECT":
            world.add_object(arg)
        elif cmd == "ADD_CONSTRAINT":
            world.add_constraint(arg)
        elif cmd == "ADD_CONDITION":
            world.add_condition(arg)
    # Clear UI commands once applied
    ui_commands.clear()

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

        # Update simulation
        world.update(dt)

        # Clear screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Draw world
        world.draw()

        pygame.display.flip()

    return {"next": "MAIN_MENU"}

def simulation_edit(SCREEN, state):
    WIDTH, HEIGHT = SCREEN
    VIDEO_HEIGHT = HEIGHT
    VIDEO_WIDTH = 9 * (HEIGHT / 16)
    CENTER_X = WIDTH / 2

    pygame.display.set_caption("World Editor (UI)")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    running = True
    start_simulation = False

    font = pygame.font.SysFont("Arial", 24)

    # Start Simulation button
    start_button = Button(
        image=None,
        pos=(WIDTH / 2, HEIGHT * 0.9),
        text_input="START SIMULATION",
        font=pygame.font.Font(FONT_PATH, 60),
        base_color="#d7fcd4",
        hovering_color="White"
    )

    # Left panel width
    LEFT_PANEL_WIDTH = CENTER_X - VIDEO_WIDTH / 2
    PANEL_PADDING = 20
    ROW_HEIGHT = 40

    # Dropdowns
    object_dropdown = Dropdown(
        pos=(LEFT_PANEL_WIDTH / 10, 50),
        width=LEFT_PANEL_WIDTH - 2 * PANEL_PADDING,
        options=["Ball", "Ring"],
        font=font,
        base_color="#AAAAAA",
        hovering_color="White",
        text_input="Objects",
        on_select=queue_object
    )

    constraint_dropdown = Dropdown(
        pos=(LEFT_PANEL_WIDTH / 10, 50 + ROW_HEIGHT + 10),
        width=LEFT_PANEL_WIDTH - 2 * PANEL_PADDING,
        options=["Gravity"],
        font=font,
        base_color="#AAAAAA",
        hovering_color="White",
        text_input="Constraints",
        on_select=queue_constraint
    )

    condition_dropdown = Dropdown(
        pos=(LEFT_PANEL_WIDTH / 10, 50 + 2 * (ROW_HEIGHT + 10)),
        width=LEFT_PANEL_WIDTH - 2 * PANEL_PADDING,
        options=["BallCount"],
        font=font,
        base_color="#AAAAAA",
        hovering_color="White",
        text_input="Conditions",
        on_select=queue_condition
    )

    dropdowns = [object_dropdown, constraint_dropdown, condition_dropdown]

    while running and not start_simulation:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.checkForInput(mouse_pos):
                    start_simulation = True
            # Pass events to dropdowns
            for dd in dropdowns:
                dd.handle_event(event, mouse_pos)

        # Draw left panel background & border
        panel_rect = pygame.Rect(0, 0, LEFT_PANEL_WIDTH, HEIGHT)
        pygame.draw.rect(screen, (50, 50, 50), panel_rect)
        pygame.draw.rect(screen, (200, 200, 200), panel_rect, 3)

        # Dynamically update dropdown positions
        current_y = 50
        for dd in dropdowns:
            dd.y_pos = current_y + dd.rect.height / 2  # center position
            dd.rect.center = (dd.x_pos, dd.y_pos)
            dd.text_rect.center = (dd.x_pos, dd.y_pos)
            # Update option button positions
            for i, btn in enumerate(dd.option_buttons):
                btn.y_pos = dd.y_pos + (i + 1) * (dd.rect.height + 5)
                btn.rect.center = (btn.x_pos, btn.y_pos)
                btn.text_rect.center = (btn.x_pos, btn.y_pos)
            current_y += dd.total_height() + 10  # spacing between dropdowns

        # Draw dropdowns
        for dd in dropdowns:
            dd.update(screen)

        # Draw start button
        start_button.changeColor(mouse_pos)
        start_button.update(screen)

        pygame.display.flip()

    return {"next": "SIMULATION"}
