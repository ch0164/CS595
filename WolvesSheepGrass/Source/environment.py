"""

Title:          Environment

Description:    The objective of this file is to define the environment of the simulation,
                i.e. which grids contain grass or dirt patches.

"""

# Project Related Imports
from Utilities.common_imports import *
from Utilities.constants import *

# Global Variable Declarations

# IDE Likes Two Empty Lines Before Class Definition


class Environment:

    def __init__(self, world_size, grass_regrowth_time):
        self.world_size = world_size  # How many rows/columns there are
        self.regrowth_time = grass_regrowth_time  # How many grass patches should be generated per time step
        self.grid_count = world_size * world_size  # How many individual grids there are in the world
        self.terrain = np.zeros((world_size, world_size), dtype=bool)  # Boolean matrix -- 1 = grass, 0 = dirt

        # Randomly generate half of the terrain with grass and half with dirt.
        for i in range(self.grid_count // 2):
            row, col = random.randint(0, world_size - 1), random.randint(0, world_size - 1)
            if not self.terrain[row][col]:
                self.terrain[row][col] = True
            else:
                continue

    def print_world(self):
        # Print world for reference.
        for row in range(self.world_size):
            for col in range(self.world_size):
                if self.terrain[row][col]:
                    print(GREEN_FONT + "🟩", end="")
                else:
                    print(BROWN_FONT + "🟫", end="")
            print()
        print(WHITE_FONT)  # Set font back to default

# IDE Likes Empty Line At End Of File
