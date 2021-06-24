from wsg_model import *
from wsg_visualization import *

# Set environment parameters.
world_width, world_length = 25, 25
grass_regrowth_time = 30

# Set initial conditions and parameters.
wolf_count, sheep_count = 50, 100
wolf_food_gain, sheep_food_gain = 20, 4
wolf_reproduction, sheep_reproduction = 0.05, 0.04
max_sheep = 10_000


def run_simulation():

    # Initialize the model
    model = WolfSheepGrass(world_width, world_length, grass_regrowth_time, wolf_count, sheep_count,
                           wolf_food_gain, sheep_food_gain, wolf_reproduction, sheep_reproduction, max_sheep)
    # Run the model.
    model.run_model()


if __name__ == "__main__":
    run_simulation()
    # run_server(world_width, world_length)

