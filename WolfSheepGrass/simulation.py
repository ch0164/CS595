from Utilities.constants import *
from Utilities.common_imports import *
from model import *

def run_simulation():
    # Set environment parameters.
    world_width, world_length = 25, 25
    grass_regrowth_time = 30

    # Set initial conditions and parameters.
    wolf_count, sheep_count = 0, 20
    wolf_food_gain, sheep_food_gain = 20, 4
    wolf_reproduction, sheep_reproduction = 0.05, 0.04
    max_sheep = 10_000

    # Initialize the model
    model = WolfSheepGrass(world_width, world_length, grass_regrowth_time, wolf_count, sheep_count,
                           wolf_food_gain, sheep_food_gain, wolf_reproduction, sheep_reproduction, max_sheep)

    model.run_model()


if __name__ == "__main__":
    run_simulation()