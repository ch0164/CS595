from wsg_agent import *                         # Import the agents used in the model.
from mesa import Model                          # Import the Model base class.
from mesa.time import RandomActivation          # Import the scheduler for each agent.
from mesa.space import MultiGrid                # Import the grid to position and move agents for the model.
from mesa.datacollection import DataCollector   # Import the datacollector to track population count over each step.

# Define constants for patches of grass and dirt.
GRASS_PATCH, DIRT_PATCH = True, False


class WolfSheepGrass(Model):

    def __init__(self, width: int, height: int,
                 grass_regrowth_rate: int, initial_wolves: int, initial_sheep: int,
                 wolf_food_gain: int, sheep_food_gain: int,
                 wolf_reproduction_rate: float, sheep_reproduction_rate: float, max_sheep: int):
        """
        Initializes the WolfSheepGrass model.
        :param width: Width of the grid-world (i.e. horizontal length).
        :param height: Height of the grid-world (i.e. vertical length).
        :param grass_regrowth_rate: An integer value between 0 and 100 used to determine when dirt grows to grass.
        :param initial_wolves: An integer value between 0 and 250 which determines the initial number of wolves.
        :param initial_sheep: An integer value between 0 and 250 which determines the initial number of sheep.
        :param wolf_food_gain: An integer value which determines how much energy the wolf gains from eating.
        :param sheep_food_gain: An integer value which determines how much energy the sheep gains from eating.
        :param wolf_reproduction_rate: A floating-point value between 0 and 0.2; determines probability to reproduce.
        :param sheep_reproduction_rate: A floating-point value between 0 and 0.2; determines probability to reproduce.
        :param max_sheep: The maximum number of sheep which can be alive at one time; if exceeded, the simulation stops.
        """

        # Initialize the Model base class.
        super().__init__()

        # Clear output files for new test run.
        with open("../Graphics/wsg.csv", "w") as wsg_file:
            wsg_file.writelines("Time,Agent,x,y,Energy\n")
        with open("../Graphics/plot.csv", "w") as plot_file:
            plot_file.writelines("Time,Sheep,Wolves,Grass,Dirt\n")

        # Keep track of the current time step.
        self.time = 0

        # Width and height define the x- and y-dimensions of the world, respectively.
        self.width, self.height = width, height

        # Don't let the number of sheep grow too large.
        self.max_sheep = max_sheep

        # Instantiate discrete, toroidal grid to contain all wolves, sheep, and grass.
        self.grid = MultiGrid(width, height, True)

        # Initialize the scheduler, which activates agents in a random order per step/tick.
        self.sheep_schedule = RandomActivation(self)
        self.wolf_schedule = RandomActivation(self)
        self.patch_schedule = RandomActivation(self)

        # Add initial sheep (they move first in the NetLogo simulation).
        for _ in range(initial_sheep):
            # On startup, position is a random floating-point coordinate between 0 and the max dimension of the world.
            x_pos = self.random.uniform(0, width)
            y_pos = self.random.uniform(0, height)

            # Instantiate the new Sheep object with the given coordinates and parameters.
            sheep = Sheep(self, x_pos, y_pos, sheep_food_gain, sheep_reproduction_rate)

            # Add the new sheep to its respective scheduler.
            self.sheep_schedule.add(sheep)

            # Place the sheep on the agent grid using integer coordinates.
            self.grid.place_agent(sheep, self.integer_position(x_pos, y_pos))

        # Add initial wolves.
        for _ in range(initial_wolves):
            # On startup, position is a random floating-point coordinate between 0 and the max dimension of the world.
            x_pos = self.random.uniform(0, width)
            y_pos = self.random.uniform(0, height)

            # Instantiate the new Wolf object with the given coordinates and parameters.
            wolf = Wolf(self, x_pos, y_pos, wolf_food_gain, wolf_reproduction_rate)

            # Add the new wolf to its respective scheduler.
            self.wolf_schedule.add(wolf)

            # Place the wolf on the agent grid using integer coordinates.
            self.grid.place_agent(wolf, self.integer_position(x_pos, y_pos))

        # Initialize environment by filling terrain with grass and dirt patches.
        for x in range(width):
            for y in range(height):
                # Instantiate the new Patch object with the given grass regrowth rate.
                patch = Patch(self, grass_regrowth_rate, (x, y))

                # Add the new patch of grass or dirt to its respective scheduler.
                self.patch_schedule.add(patch)

                # Place the patch of grass or dirt at the given coordinate.
                self.grid.place_agent(patch, (x, y))

        # Define DataCollector instance, which tracks the population of wolves and sheep as well as the number of grass.
        self.dc = DataCollector(model_reporters={"Sheep Count": self.get_sheep_count,
                                                 "Wolf Count": self.get_wolf_count,
                                                 "Grass / 5 Count": self.get_grass_count},
                                agent_reporters={})

    def step(self):
        """This method provides the logic loop for each step of the model."""

        # Collect sheep, wolf, and grass populations.
        self.dc.collect(self)

        # Output sheep, wolf, and grass locations and energy to .csv file.
        output_string = "{},{},{},{},{}\n"
        with open("../Graphics/wsg.csv", "a") as wsg_file:
            # Output grass locations
            for grass in [agent for agent in self.patch_schedule.agents if agent.patch_color is GRASS_PATCH]:
                wsg_file.writelines(output_string.format(self.time, "grass", grass.x, grass.y, ""))
            # Output wolf locations and energy.
            for wolf in self.wolf_schedule.agents:
                x, y = wolf.x_pos % self.width, wolf.y_pos % self.height
                wsg_file.writelines(output_string.format(self.time, "wolf", x, y, wolf.energy))
            # Output sheep locations and energy.
            for sheep in self.sheep_schedule.agents:
                x, y = sheep.x_pos % self.width, sheep.y_pos % self.height
                wsg_file.writelines(output_string.format(self.time, "sheep", x, y, sheep.energy))

        # Output sheep, wolf, grass, and dirt populations to .csv file.
        with open("../Graphics/plot.csv", "a") as plot_file:
            wolf_count, sheep_count, grass_count = self.get_wolf_count(), self.get_sheep_count(), self.get_grass_count()
            dirt_count = self.width * self.height - grass_count * 5
            plot_file.writelines(output_string.format(self.time, sheep_count, wolf_count, grass_count * 5, dirt_count))

        # Increment the time step.
        self.time += 1

        # First, move the sheep.
        self.sheep_schedule.step()

        # Finally, move the wolves.
        self.wolf_schedule.step()

        # Finally, grow the grass. (Note: sheep have a chance to be standing on grass)
        self.patch_schedule.step()

        # Get wolf and sheep counts.
        wolf_count, sheep_count = self.get_wolf_count(), self.get_sheep_count()

        # Are the wolves and sheep annihilated?
        are_annihilated = wolf_count <= 0 and sheep_count <= 0

        # Do the sheep rule the world?
        sheep_inherit = wolf_count <= 0 and sheep_count > self.max_sheep

        if are_annihilated:
            exit(1)
        elif sheep_inherit:
            print("The sheep have inherited the world.")
            exit(2)

    def remove(self, agent):
        """
        This method defines the logic for removing an agent from the simulation after it has "died".
        :param agent: The agent which has "died", either by being eaten or by starvation.
        :return:
        """

        # Is the agent a wolf?
        if agent.label == "Wolf":
            # Remove the wolf from the scheduler and from the agent grid.
            self.grid.remove_agent(agent)
            self.wolf_schedule.remove(agent)
            del agent

        # Is the agent a sheep?
        elif agent.label == "Sheep":
            # Remove the sheep from the scheduler and from the agent grid.
            self.grid.remove_agent(agent)
            self.sheep_schedule.remove(agent)
            del agent

    def integer_position(self, x_pos: float, y_pos: float) -> tuple:
        """
        This method receives a floating-point coordinate and returns an integer coordinate (as a tuple).
        :param x_pos: The x-position of the agent as a floating-point.
        :param y_pos: The y-position of the agent as a floating-point.
        :return: The xy-coordinate of the agent as an ordered pair of integers.
        """

        return int(x_pos) % self.width, int(y_pos) % self.height

    def get_sheep_count(self) -> int:
        """
        This method returns the current population of sheep in the simulation.
        :return: An integer representing the population of sheep.
        """

        return self.sheep_schedule.get_agent_count()

    def get_wolf_count(self) -> int:
        """
        This method returns the current population of sheep in the simulation.
        :return: An integer representing the population of sheep.
        """
        return self.wolf_schedule.get_agent_count()

    def get_grass_count(self) -> float:
        """
        This method returns the current number of grass patches divided by 5 (to be closer to wolf/sheep populations).
        :return: A floating-point number representing the approximate number of grass patches divided by 5.
        """

        return len([patch for patch in self.patch_schedule.agents if patch.patch_color is GRASS_PATCH]) / 5
