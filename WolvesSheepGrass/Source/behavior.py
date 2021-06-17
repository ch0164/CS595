"""

Title:          Behavior

Description:    The objective of this file is to contain classes related to the agents' behavior; specifically,
                eating and reproducing (potentially moving as well).
"""

# Project Related Imports
from Utilities.common_imports import *
from Utilities.constants import *
from agent import *
from environment import *

# Global Variable Declarations

# IDE Likes Two Empty Lines Before Class Definition


class MoveBehavior(object):
    """
    :return:

    Description: Defines the base class for movement; movement is one space in any eight directions.
    """

    def __init__(self, agent):
        self.agent = agent

    def move(self):
        pass


class WanderBehavior(MoveBehavior):

    def __init__(self, agent):
        MoveBehavior.__init__(self, agent)

    def move(self):
        # Get current location of agent.
        current_row, current_col = self.agent.row, self.agent.col

        # Move agent in random direction.
        row_rand = random.random()
        if row_rand < 0.5:
            current_row -= 1
        else:
            current_row += 1

        col_rand = random.random()
        if col_rand < 0.5:
            current_col -= 1
        else:
            current_col += 1

        # Update agent's position to current position.
        self.agent.row, self.agent.col = current_row, current_col

        # Decrement agent's energy by one.
        self.agent.energy -= 1


class SeekBehavior(MoveBehavior):

    def __init__(self, agent, world_size):
        MoveBehavior.__init__(agent, world_size)

    def move(self):
        pass


class EatBehavior(object):

    def __init__(self, agent, food_gain, world_size):
        self.agent = agent
        self.food_gain = food_gain
        self.world_size = world_size

    def eat(self, prey_list, terrain):
        pass


class Carnivore(EatBehavior):

    def __init__(self, agent, food_gain, world_size):
        EatBehavior.__init__(self, agent, food_gain, world_size)

    def eat(self, prey_list, terrain):
        for index, prey in enumerate(prey_list):
            if self.agent.is_overlapping(prey):
                del prey_list[index]  # Eat the prey
                self.agent.energy += self.food_gain


class Herbivore(EatBehavior):

    def __init__(self, agent, food_gain, world_size):
        EatBehavior.__init__(self, agent, food_gain, world_size)

    def eat(self, prey_list, terrain):
        if self.agent.is_on_grass(terrain):
            terrain[self.agent.row % self.world_size][self.agent.col % self.world_size] = DIRT_PATCH  # Eat the grass
            self.agent.energy += self.food_gain


class ReproduceBehavior:

    def __init__(self, reproduction_rate):
        pass


# IDE Likes Empty Line At End Of File
