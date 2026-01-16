import random

from core.objects.ring import Ring
from core.objects.ball import Ball
from core.constraints.gravity import Gravity
from core.conditions.ball_count import BallCount

def resolve(value, context):
    if isinstance(value, str):
        return eval(value, {}, context)
    return value

def load_arena(data, context):
    arena_type = data["type"]

    if arena_type == "Ring":
        return Ring(
            center=(
                resolve(data["center"][0], context),
                resolve(data["center"][1], context)
            ),
            radius=data["radius"],
            arc_degree=data["arc_degree"],
            spinning_speed=data["spinning_speed"]
        )

    raise ValueError(f"Unknown arena type: {arena_type}")

def load_constraints(constraints_data):
    constraints = []

    for c in constraints_data:
        if c["type"] == "Gravity":
            constraints.append(Gravity(c["strength"]))
        else:
            raise ValueError(f"Unknown constraint type: {c['type']}")

    return constraints

def load_end_condition(data):
    if data["type"] == "BallCount":
        return BallCount(data["count"])

    raise ValueError(f"Unknown end condition type: {data['type']}")

def load_ball(data, context):
    vel = data["vel"]

    vx = random.uniform(vel["x"][0], vel["x"][1])
    vy = random.uniform(vel["y"][0], vel["y"][1])

    return Ball(
        pos=[
            resolve(data["pos"][0], context),
            resolve(data["pos"][1], context)
        ],
        vel=[vx, vy],
        radius=data["radius"],
        color=tuple(data["color"]),
        sfx=data.get("sfx"),
        vfx=data.get("vfx")
    )
