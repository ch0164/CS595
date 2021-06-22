"""

Title:          Agent

Description:    The objective of this file is to contain class definitions for this project's two agents,
                wolves and sheep.

"""

# Project Related Imports
from Utilities.common_imports import *
from Utilities.constants import *
from behavior import *
from environment import *

# Global Variable Declarations

# IDE Likes Two Empty Lines Before Class Definition


class Agent(object):

    def __init__(self, world_size):
        self.world_size = world_size
        self.symbol = ""
        self.energy = 0
        self.row = random.randint(0, world_size - 1)
        self.col = random.randint(0, world_size - 1)
        self.movement_behavior = WanderBehavior(self)
        self.eat_behavior = None
        self.reproduce_behavior = None

    def move(self, terrain=None, food_list=None, predator_list=None):
        self.movement_behavior.move(terrain, food_list, predator_list)

    def is_overlapping(self, other_agent):
        return (self.row % self.world_size == other_agent.row % self.world_size) and \
            (self.col % self.world_size == other_agent.col % self.world_size)

    def is_on_grass(self, terrain):
        # Determine whether or not the agent is on a grass patch.
        return is_grass(terrain, self.world_size, self.row, self.col)

    def at_position(self, row, col, terrain=None):
        # Determine if the agent is at the specified position.
        return self.row % self.world_size == row and self.col % self.world_size == col


class Wolf(Agent):

    def __init__(self, world_size, wolf_food_gain, wolf_reproduction):
        Agent.__init__(self, world_size)
        self.symbol = "x"
        self.energy = random.randint(0, 2 * wolf_food_gain - 1)
        self.eat_behavior = Carnivore(self, wolf_food_gain, world_size)
        self.reproduce_behavior = ReproduceBehavior(self, wolf_reproduction)

    def eat(self, prey_list, terrain):
        self.eat_behavior.eat(prey_list, terrain)

    def reproduce(self):
        return self.reproduce_behavior.reproduce()


class Sheep(Agent):

    def __init__(self, world_size, sheep_food_gain, sheep_reproduction):
        Agent.__init__(self, world_size)
        self.symbol = "o"
        self.energy = 2 * sheep_food_gain
        self.food_gain = sheep_food_gain
        self.eat_behavior = Herbivore(self, sheep_food_gain, world_size)
        self.reproduce_behavior = ReproduceBehavior(self, sheep_reproduction)

    def eat(self, prey_list, terrain):
        self.eat_behavior.eat(prey_list, terrain)

    def reproduce(self):
        return self.reproduce_behavior.reproduce()


# IDE Likes Empty Line At End Of File
