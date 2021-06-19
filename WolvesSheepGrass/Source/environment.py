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
        self.world_size = world_size
        self.terrain = [[Grass(grass_regrowth_time) for _ in range(world_size)] for _ in range(world_size)]

    def cultivate(self):
        # Determine if it is time for dirt patch to regrow into a grass patch.
        for patches in self.terrain:
            for patch in patches:
                patch.grow()

    def print_world(self, iteration):
        # Print world for reference.
        print("Iteration {}:".format(iteration + 1))
        for patches in self.terrain:
            for patch in patches:
                patch.show()
            print()
        print(WHITE_FONT)


class Grass:

    def __init__(self, grass_regrowth_time):
        self.grass_regrowth_time = grass_regrowth_time
        self.countdown = random.randint(0, grass_regrowth_time - 1)

        # There is a 50% chance upon generation that a patch is grass.
        if random.random() < 0.5:
            self.patch_color = DIRT_PATCH
        else:
            self.patch_color = GRASS_PATCH

    def grow(self):
        # If the patch is brown and countdown is not positive, set patch color to green and reset the countdown timer.
        if self.patch_color is DIRT_PATCH and self.countdown <= 0:
            self.patch_color = GRASS_PATCH
            self.countdown = self.grass_regrowth_time
        # Otherwise, decrement the countdown timer by one.
        else:
            self.countdown -= 1

    def show(self, end=""):
        if self.patch_color is GRASS_PATCH:
            print(GREEN_FONT + "🟩", end=end)
        else:
            print(BROWN_FONT + "🟫", end=end)


def get_patch(terrain, world_size, row, col):
    # Return the patch object specified by the position passed.
    return terrain[row % world_size][col % world_size]


def is_grass(terrain, world_size, row, col):
    # Determine whether or not the specified location is a grass patch.
    return get_patch(terrain, world_size, row, col).patch_color is GRASS_PATCH

# IDE Likes Empty Line At End Of File
