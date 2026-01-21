# library/sim_loader.py
import json

from library.factories import (
    load_arena,
    load_constraints,
    load_end_condition,
    load_ball
)

from core.world.world import World

def load_simulation_from_json(path_or_config, width, height, recording=False):
    if isinstance(path_or_config, str):
        with open(path_or_config, "r") as f:
            config = json.load(f)
    elif isinstance(path_or_config, dict):
        config = path_or_config
    else:
        raise TypeError(
            "load_simulation_from_json expects a file path (str) or a dict"
        )

    context = {"WIDTH": width, "HEIGHT": height}

    arena = load_arena(config["arena"], context)

    world = World(
        arena=arena,
        width=width,
        height=height,
        constraints=load_constraints(config["world"]["constraints"]),
        end_condition=load_end_condition(config["world"]["end_condition"]),
        recording_enabled = recording
    )

    for ball_cfg in config.get("balls", []):
        world.spawn(load_ball(ball_cfg, context))

    return world