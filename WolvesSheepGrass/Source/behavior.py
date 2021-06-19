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


class FleeBehavior(MoveBehavior):

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
                # Eat the prey
                del prey_list[index]  # The sheep "dies" when it is deleted from the list
                self.agent.energy += self.food_gain


class Herbivore(EatBehavior):

    def __init__(self, agent, food_gain, world_size):
        EatBehavior.__init__(self, agent, food_gain, world_size)

    def eat(self, prey_list, terrain):
        if self.agent.is_on_grass(terrain):
            # Eat the grass
            patch = get_patch(terrain, self.world_size, self.agent.row, self.agent.col)
            patch.patch_color = DIRT_PATCH
            self.agent.energy += self.food_gain


# TODO: Maybe we could add genetics into this...
#  The child_agent could inherit a different movement behavior than the parent, i.e. recessive gene.
class ReproduceBehavior:

    def __init__(self, agent, reproduction_rate):
        self.agent = agent
        self.reproduction_rate = reproduction_rate

    def reproduce(self):
        # Produce a random number between 0 and 100.
        rand_reproduce = random.random() * 100

        # If the random number is less than the agent's reproduction rate, reproduce.
        child_agent = None

        if rand_reproduce < self.reproduction_rate:
            child_agent = copy.deepcopy(self.agent)  # Spawn a child of the agent.
            child_agent.energy = 2 * child_agent.food_gain  # Set the child's initial energy.
            self.agent.energy /= 2  # Divide parent agent's energy by half.
            child_agent.move()  # Move the child agent.

        # Return the child.
        return child_agent


# IDE Likes Empty Line At End Of File
