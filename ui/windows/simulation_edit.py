import pygame
from ui.widgets.button import Button
from ui.widgets.dropdown import Dropdown
from ui.widgets.checkbox import CheckBox
from library.sim_loader import load_simulation_from_json
from library.sim_file_handler import *

FONT_PATH = "ui/assets/OpenSans.ttf"

ui_commands = []

def pygame_display(width, height):
    return pygame.display.set_mode((width, height), 
        pygame.RESIZABLE)

def queue_object(obj_type):
    ui_commands.append(("ADD_OBJECT", obj_type))

def queue_constraint(c_type):
    ui_commands.append(("ADD_CONSTRAINT", c_type))

def queue_condition(cond_type):
    ui_commands.append(("ADD_CONDITION", cond_type))

def option(label):
    return Button(
        image=None,
        pos=(0,0),
        text_input=label,
        font=pygame.font.SysFont("Arial", 24),
        base_color="#AAAAAA",
        hovering_color="White",
    )

def simulation_edit(SCREEN, state):
    WIDTH, HEIGHT = SCREEN
    VIDEO_HEIGHT = HEIGHT
    VIDEO_WIDTH = 9 * (HEIGHT / 16)
    CENTER_X = WIDTH / 2

    pygame.display.set_caption("World Editor (UI)")
    screen = pygame_display(WIDTH, HEIGHT)
    font_button = pygame.font.SysFont("Arial", 24)

    running = True
    start_simulation = False

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
    RIGHT_PANEL_WIDTH = LEFT_PANEL_WIDTH
    PANEL_PADDING = 20
    ROW_HEIGHT = 40

    # Dropdowns
    ball_dropdown = Dropdown(
        pos=(30, 0),
        width=LEFT_PANEL_WIDTH - 2 * PANEL_PADDING,
        options=[
            option("Set Radius"),
            option("Set Mass"),
        ],
        font=font_button,
        base_color="#AAAAAA",
        hovering_color="White",
        text_input="Ball",
        on_select=queue_object,
    )

    ring_dropdown = Dropdown(
        pos=(30, 0),
        width=LEFT_PANEL_WIDTH - 2 * PANEL_PADDING,
        options=[
            option("Set Radius"),
        ],
        font=font_button,
        base_color="#AAAAAA",
        hovering_color="White",
        text_input="Ring",
        on_select=queue_object,
    )

    gravity_dropdown = Dropdown(
        pos=(30, 0),
        width=LEFT_PANEL_WIDTH - 2 * PANEL_PADDING,
        options=[
            option("Enable Gravity"),
            option("Set Strength"),
        ],
        font=font_button,
        base_color="#AAAAAA",
        hovering_color="White",
        text_input="Gravity",
        on_select=queue_constraint,
    )


    object_dropdown = Dropdown(
        pos=(LEFT_PANEL_WIDTH / 10, 50),
        width=LEFT_PANEL_WIDTH - 2 * PANEL_PADDING,
        options=[ball_dropdown, ring_dropdown],
        font=font_button,
        base_color="#AAAAAA",
        hovering_color="White",
        text_input="Objects",
    )

    constraint_dropdown = Dropdown(
        pos=(LEFT_PANEL_WIDTH / 10, 50 + ROW_HEIGHT + 10),
        width=LEFT_PANEL_WIDTH - 2 * PANEL_PADDING,
        options=[gravity_dropdown],
        font=font_button,
        base_color="#AAAAAA",
        hovering_color="White",
        text_input="Constraints",
    )

    condition_dropdown = Dropdown(
        pos=(LEFT_PANEL_WIDTH / 10, 50 + 2 * (ROW_HEIGHT + 10)),
        width=LEFT_PANEL_WIDTH - 2 * PANEL_PADDING,
        options=[
            option("Ball Count"),
        ],
        font=font_button,
        base_color="#AAAAAA",
        hovering_color="White",
        text_input="Conditions",
        on_select=queue_condition,
    )


    # Record
    record_checkbox = CheckBox(
        pos=(CENTER_X + VIDEO_WIDTH / 2 + 40, 60),
        label="Enable Recording (video saved to record/saved_videos)",
        font=font_button
    )

    dropdowns = [object_dropdown, constraint_dropdown, condition_dropdown]

    while running and not start_simulation:
        mouse_pos = pygame.mouse.get_pos()

        # ----- Event Handling -----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                record_checkbox.handle_event(event)
                if start_button.checkForInput(mouse_pos):
                    start_simulation = True

            # Pass events to dropdowns (parent handles children)
            for dd in dropdowns:
                dd.handle_event(event, mouse_pos)

        # ----- Layout top-level dropdowns -----
        current_y = 50
        for dd in dropdowns:
            dd.y_pos = current_y
            dd.update_rect()          # update rect for this position
            dd.layout_options()       # layout children based on parent rect
            current_y += dd.total_height() + dd.spacing

        # ----- Draw Panels -----
        # Left panel
        panel_rect = pygame.Rect(0, 0, LEFT_PANEL_WIDTH, HEIGHT)
        pygame.draw.rect(screen, (50, 50, 50), panel_rect)
        pygame.draw.rect(screen, (200, 200, 200), panel_rect, 3)

        # Right panel
        panel_rect = pygame.Rect(CENTER_X + (VIDEO_WIDTH / 2), 0, RIGHT_PANEL_WIDTH, HEIGHT)
        pygame.draw.rect(screen, (50, 50, 50), panel_rect)
        pygame.draw.rect(screen, (200, 200, 200), panel_rect, 3)

        # ----- Draw Dropdowns -----
        for dd in dropdowns:
            dd.update(screen)

        # ----- Draw Buttons -----
        start_button.changeColor(mouse_pos)
        start_button.update(screen)
        record_checkbox.update(screen)

        pygame.display.flip()

    # Save world to JSON file

    #placeholders    
    template_path = "library/simulation_template/default.json"
    new_sim_path = create_new_sim_file(template_path)

    # Load from said JSON file
    world = load_simulation_from_json(new_sim_path, WIDTH, HEIGHT, record_checkbox.checked)

    return {
        "next": "SIMULATION",
        "world": world,
    }

