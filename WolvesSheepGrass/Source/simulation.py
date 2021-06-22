"""

Title:          Simulation

Description:    The objective of this file is to contain the logic for conducting the Wolves-Sheep-Grass simulation.

"""

# Project Related Imports
from Utilities.common_imports import *
from Utilities.constants import *
from environment import *
from agent import *

# Global Variable Declarations
row_data = []  # To contain the representation of the world data at one time as a list of strings.

# IDE Likes Two Empty Lines Before Class Definition


def run_simulation():
    # TODO: Implement scenario

    # Set simulation parameters.
    iterations, tick = 100, 0.5

    # Set environment parameters.
    # TODO: World size can differ in x and y dimensions.
    world_size, grass_regrowth_time = 10, 20

    # Initialize the environment.
    wsg_world = Environment(world_size, grass_regrowth_time)

    # Set initial conditions and parameters.
    wolf_count, sheep_count = 1, 50
    wolf_food_gain, sheep_food_gain = 20, 4
    wolf_reproduction, sheep_reproduction = 0.05, 0.04

    # Initialize wolves and sheep, the agents in the simulation.
    wolf_list = [Wolf(world_size, wolf_food_gain, wolf_reproduction) for _ in range(wolf_count)]
    sheep_list = [Sheep(world_size, sheep_food_gain, sheep_reproduction) for _ in range(sheep_count)]
    agent_list = wolf_list + sheep_list

    # Run the simulation.
    for iteration in range(iterations):
        for index, agent in enumerate(agent_list):
            # Move the agent according to its movement behavior.
            agent.move(wsg_world.terrain, sheep_list, wolf_list)

            # Let the agent eat according to its diet.
            agent.eat(agent_list, wsg_world.terrain)

            # Determine if the agent should reproduce or not.
            child_agent = agent.reproduce()
            if child_agent:
                agent_list.append(child_agent)

            # Is the agent out of energy (i.e. dead)?
            if agent.energy <= 0:
                del agent_list[index]

            # Update the lists of wolves and sheep.
            wolf_list = [agent for agent in agent_list if isinstance(agent, Wolf)]
            sheep_list = [agent for agent in agent_list if isinstance(agent, Sheep)]

        # Show the terrain and the population of wolves and sheep.
        wsg_world.print_world(iteration, agent_list, len(wolf_list), len(sheep_list))

        # Cultivate the terrain with grass patches.
        wsg_world.cultivate()

        # For manual simulation only -- suspend execution to examine output.
        # time.sleep(tick)





    # Used for debugging:

    # for _ in range(1000):
    #     for index, sheep in enumerate(sheep_list):
    #         sheep.Move()
    #         if wsg_world.terrain[sheep.row % world_size][sheep.col % world_size]:
    #             print("Sheep {0} is on grass! Located at: {1}"
    #                   .format(index, str((sheep.row % world_size, sheep.col % world_size))))
    #         else:
    #             print("Sheep {0} is on dirt... Located at: {1}"
    #                   .format(index, str((sheep.row % world_size, sheep.col % world_size))))
    # wsg_world.print_world()

    # for _ in range(11):
    #     for index, wolf in enumerate(wolf_list):
    #         current_position = "(" + str(wolf.row) + ", " + str(wolf.col) + ")"
    #         wolf.Move()
    #         next_position = "(" + str(wolf.row) + ", " + str(wolf.col) + ")"
    #         print("Wolf " + str(index) + ": Current Position = " + current_position + "\tNext position = " + next_position
    #               + "\tEnergy: " + str(wolf.energy))
    #         if wolf.energy <= 0:
    #             wolf_list.pop(index)
    #         if not wolf_list:
    #             print("The wolves have all died out...")
    #             break


if __name__ == "__main__":
    run_simulation()


# IDE Likes Empty Line At End Of File
