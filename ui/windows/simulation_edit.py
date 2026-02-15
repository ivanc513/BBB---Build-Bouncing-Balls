import pygame
from ui.widgets.button import Button
from ui.widgets.dropdown import Dropdown
from ui.widgets.checkbox import CheckBox
from ui.widgets.highlight_dropdown import HighlightDropdown
from ui.widgets.sliderbutton import SliderButton
from library.sim_loader import load_simulation_from_json
from library.sim_file_handler import *
import json


FONT_PATH = "ui/assets/OpenSans.ttf"
ADJUST_SPIN_SPEED = 1000
ADJUST_GRAVITY = 5

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

def option(label, min_val, max_val):
    return SliderButton(
        image=None,
        pos=(0,0),
        text_input=label,
        font=pygame.font.SysFont("Arial", 24),
        base_color="#AAAAAA",
        hovering_color="White",
        min_value = min_val,
        max_value = max_val,
        start_value = (max_val + min_val) / 2
    )
    
def extract_ui_values(dropdowns, record_checkbox):
    """
    Capture UI state only for highlighted dropdown options and their slider values.
    """
    data = {
        "arena": {},
        "world": {
            "constraints": [],
            "end_condition": {}
        },
        "balls": [],
        "recording_enabled": record_checkbox.checked
    }

    for dd in dropdowns:
        for option in dd.options:  # each option is a HighlightDropdown
            # Only process if the option is currently highlighted
            #if not getattr(option, "toggled", False):
             #   continue

            # Extract slider values
            slider_data = {slider.text_input: slider.value for slider in option.options}

            # Map objects (balls)
            if dd.text_input == "Objects":
                ball = {
                    "pos": ["WIDTH/2", "HEIGHT/2 - 120"],  # placeholder, could be dynamic later
                    "vel": {"x": [-4, 4], "y": [-1, 1]},
                    "radius": (slider_data.get("Set Radius", 5)), 
                    "color": [1.0, 0.0, 0.0],
                    "sfx": None,
                    "vfx": None
                }
                data["balls"].append(ball)

            # Map arena
            elif dd.text_input == "Arena":
                arena_type = option.text_input
                data["arena"] = {
                    "type": arena_type,
                    "center": ["WIDTH/2", "HEIGHT/2"],
                    "radius": slider_data.get("Set Radius", 100),
                    "arc_degree": slider_data.get("Set Arc", 60),
                    "spinning_speed": slider_data.get("Set Speed", 0) / ADJUST_SPIN_SPEED
                }

            # Map constraints
            elif dd.text_input == "Constraints":
                constraint = {"type": option.text_input}
                if "Set Strength" in slider_data:
                    constraint["strength"] = slider_data["Set Strength"] / ADJUST_GRAVITY
                data["world"]["constraints"].append(constraint)

            # Map conditions
            elif dd.text_input == "Conditions":
                condition = {"type": option.text_input}
                if "End Count" in slider_data:
                    condition["count"] = slider_data["End Count"]
                data["world"]["end_condition"] = condition

    return data

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
    ball_dropdown = HighlightDropdown(
        pos=(30, 0),
        width=LEFT_PANEL_WIDTH - 2 * PANEL_PADDING,
        options=[
            option("Set Radius", 0.1, 10.0),
        ],
        font=font_button,
        base_color="#AAAAAA",
        hovering_color="White",
        highlight_color=(255,255,0),
        text_input="Ball",
        on_select=queue_object,
    )

    ring_dropdown = HighlightDropdown(
        pos=(30, 0),
        width=LEFT_PANEL_WIDTH - 2 * PANEL_PADDING,
        options=[
            option("Set Radius", 150, 300),
            option("Set Speed", 1, 100),
            option("Set Arc", 1, 360)
        ],
        font=font_button,
        base_color="#AAAAAA",
        hovering_color="White",
        highlight_color=(255,255,0),
        text_input="Ring",
        on_select=queue_object,
    )

    gravity_dropdown = HighlightDropdown(
        pos=(30, 0),
        width=LEFT_PANEL_WIDTH - 2 * PANEL_PADDING,
        options=[
            option("Set Strength", 1, 100),
        ],
        font=font_button,
        base_color="#AAAAAA",
        hovering_color="White",
        highlight_color=(255,255,0),
        text_input="Gravity",
        on_select=queue_constraint,
    )
    
    ball_count_dropdown = HighlightDropdown(
        pos=(30, 0),
        width=LEFT_PANEL_WIDTH - 2 * PANEL_PADDING,
        options=[option("End Count", 1, 1000)],
        font=font_button,
        base_color="#AAAAAA",
        hovering_color="White",
        highlight_color=(255,255,0),
        text_input="BallCount",
        on_select=queue_constraint,
    )


    object_dropdown = Dropdown(
        pos=(LEFT_PANEL_WIDTH / 7, 50),
        width=LEFT_PANEL_WIDTH - 2 * PANEL_PADDING,
        options=[ball_dropdown],
        font=font_button,
        base_color="#AAAAAA",
        hovering_color="White",
        text_input="Objects",
    )
    
    arena_dropdown = Dropdown(
        pos=(LEFT_PANEL_WIDTH / 7, 50 + 5),
        width=LEFT_PANEL_WIDTH - 2 * PANEL_PADDING,
        options=[ring_dropdown],
        font=font_button,
        base_color="#AAAAAA",
        hovering_color="White",
        text_input="Arena",
    )

    constraint_dropdown = Dropdown(
        pos=(LEFT_PANEL_WIDTH / 7, 50 + ROW_HEIGHT + 10),
        width=LEFT_PANEL_WIDTH - 2 * PANEL_PADDING,
        options=[gravity_dropdown],
        font=font_button,
        base_color="#AAAAAA",
        hovering_color="White",
        text_input="Constraints",
    )

    condition_dropdown = Dropdown(
        pos=(LEFT_PANEL_WIDTH / 7, 50 + 2 * (ROW_HEIGHT + 10)),
        width=LEFT_PANEL_WIDTH - 2 * PANEL_PADDING,
        options=[ball_count_dropdown],
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

    dropdowns = [object_dropdown, arena_dropdown, constraint_dropdown, condition_dropdown]

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
    ui_state = extract_ui_values(dropdowns, record_checkbox)

    save_path = "library/simulation_template/user_sim.json"
    with open(save_path, "w") as f:
        json.dump(ui_state, f, indent=2)

    new_sim_path = create_new_sim_file(save_path)

    # Load from said JSON file
    world = load_simulation_from_json(new_sim_path, WIDTH, HEIGHT, record_checkbox.checked)

    return {
        "next": "SIMULATION",
        "world": world,
    }

