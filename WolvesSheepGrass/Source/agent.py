"""

Title:          Agent

Description:    The objective of this file is to contain class definitions for this project's two agents,
                wolves and sheep.

"""

# Project Related Imports
from Utilities.common_imports import *
from Utilities.constants import *
from behavior import *

# Global Variable Declarations

# IDE Likes Two Empty Lines Before Class Definition


class Agent(object):

    def __init__(self, world_size):
        self.world_size = world_size
        self.symbol = ""
        self.energy = 10
        self.row = random.randint(0, world_size - 1)
        self.col = random.randint(0, world_size - 1)
        self.movement_behavior = WanderBehavior(self)
        self.eat_behavior = None
        self.reproduce_behavior = None

    def move(self):
        self.movement_behavior.move()

    def reproduce(self):
        pass

    def is_overlapping(self, other_agent):
        return (self.row % self.world_size == other_agent.row % self.world_size) and \
            (self.col % self.world_size == other_agent.col % self.world_size)

    def is_on_grass(self, terrain):
        return terrain[self.row % self.world_size][self.col % self.world_size] is GRASS_PATCH


class Wolf(Agent):

    def __init__(self, world_size, wolf_food_gain, wolf_reproduction):
        Agent.__init__(self, world_size)
        self.symbol = "x"
        self.eat_behavior = Carnivore(self, wolf_food_gain, world_size)
        self.reproduce_behavior = ReproduceBehavior(wolf_reproduction)

    def eat(self, prey_list, terrain):
        self.eat_behavior.eat(prey_list, terrain)


class Sheep(Agent):

    def __init__(self, world_size, sheep_food_gain, sheep_reproduction):
        Agent.__init__(self, world_size)
        self.symbol = "o"
        self.food_gain = sheep_food_gain
        self.eat_behavior = Herbivore(self, sheep_food_gain, world_size)
        self.reproduce_behavior = ReproduceBehavior(sheep_reproduction)

    def eat(self, prey_list, terrain):
        self.eat_behavior.eat(prey_list, terrain)


# IDE Likes Empty Line At End Of File
