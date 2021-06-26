from mesa import Agent  # Import the base Agent class.
import numpy as np      # Import to use trigonometric functions for movement.

# Define constants for patches of grass and dirt.
GRASS_PATCH, DIRT_PATCH = True, False


class Animal(Agent):
    """Base class for animals."""

    def __init__(self, model, x_pos: float, y_pos: float, food_gain: int, reproduction_rate: float):
        """
        Initializes the base Animal class.
        :param model: The WolfSheepGrass model used for the simulation.
        :param x_pos: A floating-point coordinate between 0 and the width of the world.
        :param y_pos: A floating-point coordinate between 0 and the length of the world.
        :param food_gain: An integer value which determines how much energy the animal gains from eating.
        :param reproduction_rate: A floating-point value between 0 and 0.2; determines probability to reproduce.
        """

        # Initialize the Agent base class.
        super().__init__(model.next_id(), model)

        # Provide a label for the animal's type.
        self.label = ""

        # The animal moves around using floating-point coordinates.
        self.x_pos, self.y_pos = x_pos, y_pos

        # The animal moves according to its direction. On startup, it is a random direction between 0 and 360 degrees.
        self.direction = self.model.random.uniform(0, 2 * np.pi)

        # The animal gains a specified amount of energy from eating sheep, and has a specified chance of reproduction.
        self.food_gain, self.reproduction_rate = food_gain, reproduction_rate

        # The animal's energy is set between 0 and twice its food gain.
        self.energy = 2 * self.model.random.randrange(0, food_gain)

        # Visualization variable for determining if the animal has just spawned in.
        self.just_spawned = False

    def step(self):
        """This method provides the logic loop for the animal."""

        # Move the animal.
        self.move()

        # Deplete energy by 1 unit.
        self.energy -= 1

        # Have the animal eat sheep (if animal is a wolf) or eat grass (if animal is a sheep).
        self.eat()

        # Check for death from starvation.
        if self.energy <= 0:
            self.model.remove(self)

        # Reproduce.
        self.reproduce()

    def move(self):
        """This method provides the logic for moving an animal."""

        # Turn left between 0 to 50 degrees (or 5pi/18 radians).
        self.direction += self.model.random.uniform(0, 5 * np.pi / 18)

        # Turn right between 0 to 50 degrees (or 5pi/18 radians).
        self.direction -= self.model.random.uniform(0, 5 * np.pi / 18)

        # Move forward by one step.
        self.x_pos += np.cos(self.direction)
        self.y_pos += np.sin(self.direction)

        # Make sure position is not negative. If it is, loop around to the other side.
        if self.x_pos < 0:
            self.x_pos = self.model.width + self.x_pos
        if self.y_pos < 0:
            self.y_pos = self.model.height + self.y_pos

        # Move the animal on the grid.
        self.model.grid.move_agent(self, self.model.integer_position(self.x_pos, self.y_pos))

    def reproduce(self):
        """This method provides the logic for allowing an animal to reproduce."""

        # If a number between 0 and 1 is less than the animal's reproduction rate, reproduce.
        if self.model.random.uniform(0, 1) < self.reproduction_rate:
            # Divide parent's energy by half.
            self.energy /= 2

            # Create one new animal of the parent's type.
            if self.label == "Sheep":
                child_agent = Sheep(self.model, self.x_pos, self.y_pos, self.food_gain, self.reproduction_rate)
            else:
                child_agent = Wolf(self.model, self.x_pos, self.y_pos, self.food_gain, self.reproduction_rate)
            child_agent.just_spawned = True

            # Rotate the new animal between 0 and 360 degrees.
            child_agent.direction += self.model.random.uniform(0, 2 * np.pi)

            # Move the new animal forward by one step.
            child_agent.x_pos += np.cos(child_agent.direction)
            child_agent.y_pos += np.sin(child_agent.direction)

            # Make sure position is not negative. If it is, loop around to the other side.
            if child_agent.x_pos < 0:
                child_agent.x_pos = self.model.width + child_agent.x_pos
            if child_agent.y_pos < 0:
                child_agent.y_pos = self.model.height + child_agent.y_pos

            # Add the animal to the scheduler.
            if self.label == "Sheep":
                self.model.sheep_schedule.add(child_agent)
            else:
                self.model.wolf_schedule.add(child_agent)

            # Add the animal to the grid.
            self.model.grid.place_agent(child_agent, self.model.integer_position(child_agent.x_pos, child_agent.y_pos))


class Wolf(Animal):
    """Class which defines the Wolf agent."""

    def __init__(self, model, x_pos: float, y_pos: float, food_gain: int, reproduction_rate: float):
        """
        Initializes the Wolf class.
        :param model: The WolfSheepGrass model used for the simulation.
        :param x_pos: A floating-point coordinate between 0 and the width of the world.
        :param y_pos: A floating-point coordinate between 0 and the length of the world.
        :param food_gain: An integer value which determines how much energy the wolf gains from eating.
        :param reproduction_rate: A floating-point value between 0 and 0.2; determines probability to reproduce.
        """

        # Initialize the Animal base class.
        super().__init__(model, x_pos, y_pos, food_gain, reproduction_rate)

        # Label the animal as a Wolf.
        self.label = "Wolf"

    def eat(self):
        """This method provides the logic for the eating behavior of wolves."""

        # Get a list of all sheep on the same patch as the wolf.
        int_pos = self.model.integer_position(self.x_pos, self.y_pos)
        sheep_list = [agent for agent in self.model.grid.get_cell_list_contents([int_pos]) if agent.label == "Sheep"]

        # If sheep were found, eat one of the sheep. If none are found, end action.
        if sheep_list:
            # Select one sheep at random.
            sheep = self.model.random.choice(sheep_list)

            # "Kill" the sheep.
            self.model.remove(sheep)

            # Add energy from eating the sheep.
            self.energy += self.food_gain


class Sheep(Animal):
    """Class which defines the Sheep agent."""

    def __init__(self, model, x_pos: float, y_pos: float, food_gain: int, reproduction_rate: float):
        """
        :param model: The WolfSheepGrass model used for the simulation.
        :param x_pos: A floating-point coordinate between 0 and the width of the world.
        :param y_pos: A floating-point coordinate between 0 and the length of the world.
        :param food_gain: An integer value which determines how much energy the sheep gains from eating.
        :param reproduction_rate: A floating-point value between 0 and 0.2; determines probability to reproduce.
        """

        # Initialize the Animal base class.
        super().__init__(model, x_pos, y_pos, food_gain, reproduction_rate)

        # Label the animal as a Sheep.
        self.label = "Sheep"

    def eat(self):
        """This method provides the logic for the eating behavior of sheep."""

        # Get the patch at the sheep's position.
        int_pos = self.model.integer_position(self.x_pos, self.y_pos)
        x, y = int_pos
        int_pos = (x % self.model.width, y % self.model.height)
        patch = [agent for agent in self.model.grid.get_cell_list_contents([int_pos]) if agent.label == "Patch"][0]

        # If the patch has grass, eat it. Otherwise, end action.
        if patch.patch_color is GRASS_PATCH:
            # The grass is gone, so set the patch to dirt.
            patch.patch_color = DIRT_PATCH

            # Add energy from eating the grass.
            self.energy += self.food_gain


class Patch(Agent):

    def __init__(self, model, grass_regrowth_time: int, pos: tuple):
        """
        Initializes the Patch class used for representing grass and dirt.
        :param model: The WolfSheepGrass model used in the simulation.
        :param grass_regrowth_time: An integer value between 0 and 100 used to determine when dirt grows to grass.
        :param pos: The xy-coordinate of the patch. Note: x and y are integers, not floating-point numbers.
        """

        # Initialize the Agent base class.
        super().__init__(model.next_id(), model)

        # The patch's location on the grid.
        self.x, self.y = pos

        # Label the agent as a Patch.
        self.label = "Patch"

        # Grass regrowth time defines how many steps a patch of dirt will take before growing grass.
        self.grass_regrowth_time = grass_regrowth_time

        # Countdown is used to determine when grass grows back. Strictly less than grass regrowth time.
        self.countdown = self.model.random.randint(0, grass_regrowth_time)

        # There is a 50% chance upon generation that a patch is grass.
        if self.model.random.uniform(0, 1) < 0.5:
            self.patch_color = DIRT_PATCH
        else:
            self.patch_color = GRASS_PATCH

    def step(self):
        """This method provides the logic loop for each patch."""

        # Grow this patch of grass for every step.
        self.grow()

    def grow(self):
        """This method provides the logic for growing patches of dirt into patches of grass."""

        # If the patch is brown,
        if self.patch_color is DIRT_PATCH:
            # and countdown is not positive,
            if self.countdown <= 0:
                # then set patch color to green and reset the countdown timer.
                self.patch_color = GRASS_PATCH
                self.countdown = self.grass_regrowth_time

            # Otherwise, if the patch is brown, decrement its countdown timer by one.
            else:
                self.countdown -= 1
