from Utilities.common_imports import *
from Utilities.constants import *
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import uuid


class Wolf(Agent):

    def __init__(self, model, x_pos, y_pos, food_gain, reproduction_rate):
        super().__init__(model.next_id(), model)
        # Label the agent as a Wolf.
        self.label = "Wolf"

        # The wolf moves around using floating-point coordinates.
        self.x_pos, self.y_pos = x_pos, y_pos

        # The wolf moves according to its direction.
        self.direction = self.model.random.uniform(0, 2 * np.pi)

        # The wolf gains a specified amount of energy from eating sheep, and has a specified chance of reproduction.
        self.food_gain, self.reproduction_rate = food_gain, reproduction_rate

        # The wolf's energy is set between 0 and twice its food gain.
        self.energy = 2 * self.model.random.randrange(0, food_gain)

    def step(self):
        # Move the wolf.
        self.move()

        # Deplete energy by 1 unit.
        self.energy -= 1

        # Eat sheep in the wolf's patch.
        self.eat()

        # Check for death from starvation.
        if self.energy <= 0:
            self.model.remove(self)

        # Reproduce.
        self.reproduce()

    def move(self):
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

        # Move the agent on the grid.
        self.model.grid.move_agent(self, self.model.integer_position(self.x_pos, self.y_pos))

    def eat(self):
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

    def reproduce(self):
        # If a number between 0 and 1 is less than the agent's reproduction rate, reproduce.
        if self.model.random.uniform(0, 1) < self.reproduction_rate:
            # Divide energy by half.
            self.energy /= 2

            # Create one new agent of the parent's type.
            child_wolf = Wolf(self.model, self.x_pos, self.y_pos, self.food_gain, self.reproduction_rate)

            # Rotate the new agent between 0 and 360 degrees.
            child_wolf.direction += self.model.random.uniform(0, 2 * np.pi)

            # Move the new agent forward by one step.
            child_wolf.x_pos += np.cos(child_wolf.direction)
            child_wolf.y_pos += np.sin(child_wolf.direction)

            # Make sure position is not negative. If it is, loop around to the other side.
            if child_wolf.x_pos < 0:
                child_wolf.x_pos = self.model.width + child_wolf.x_pos
            if child_wolf.y_pos < 0:
                child_wolf.y_pos = self.model.height + child_wolf.y_pos

            # Add the agent to the scheduler.
            self.model.wolf_schedule.add(child_wolf)

            # Add the agent to the grid.
            self.model.grid.place_agent(child_wolf, self.model.integer_position(child_wolf.x_pos, child_wolf.y_pos))


class Sheep(Agent):

    def __init__(self, model, x_pos, y_pos, food_gain, reproduction_rate):
        super().__init__(model.next_id(), model)

        # Label the agent as a Sheep.
        self.label = "Sheep"

        # The sheep moves around using floating-point coordinates.
        self.x_pos, self.y_pos = x_pos, y_pos

        # The sheep moves according to its direction.
        self.direction = self.model.random.uniform(0, 2 * np.pi)

        # The sheep gains a specified amount of energy from eating grass, and has a specified chance of reproduction.
        self.food_gain, self.reproduction_rate = food_gain, reproduction_rate

        # The sheep's energy is set between 0 and twice its food gain.
        self.energy = 2 * self.model.random.randrange(0, food_gain)

    def step(self):
        # Move the sheep.
        self.move()

        # Deplete energy by 1 unit.
        self.energy -= 1

        # If there is grass on the current patch, eat it.
        self.eat()

        # Check for death from starvation.
        if self.energy <= 0:
            self.model.remove(self)

        # Reproduce.
        self.reproduce()

    def move(self):
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

        # Move the agent on the grid.
        self.model.grid.move_agent(self, self.model.integer_position(self.x_pos, self.y_pos))

    def eat(self):
        # Get the patch at the sheep's position.
        int_pos = self.model.integer_position(self.x_pos, self.y_pos)
        patch = [agent for agent in self.model.grid.get_cell_list_contents([int_pos]) if agent.label == "Patch"][0]

        # If the patch has grass, eat it. Otherwise, end action.
        if patch.patch_color is GRASS_PATCH:
            # The grass is gone, so set the patch to dirt.
            patch.patch_color = DIRT_PATCH

            # Add energy from eating the grass.
            self.energy += self.food_gain

    def reproduce(self):
        # If a number between 0 and 1 is less than the agent's reproduction rate, reproduce.
        if self.model.random.uniform(0, 1) < self.reproduction_rate:
            # Divide energy by half.
            self.energy /= 2

            # Create one new agent of the parent's type.
            child_sheep = Sheep(self.model, self.x_pos, self.y_pos, self.food_gain, self.reproduction_rate)

            # Rotate the new agent between 0 and 360 degrees.
            child_sheep.direction += self.model.random.uniform(0, 2 * np.pi)

            # Move the new agent forward by one step.
            child_sheep.x_pos += np.cos(child_sheep.direction)
            child_sheep.y_pos += np.sin(child_sheep.direction)

            # Make sure position is not negative. If it is, loop around to the other side.
            if child_sheep.x_pos < 0:
                child_sheep.x_pos = self.model.width + child_sheep.x_pos
            if child_sheep.y_pos < 0:
                child_sheep.y_pos = self.model.height + child_sheep.y_pos

            # Add the agent to the scheduler.
            self.model.sheep_schedule.add(child_sheep)

            # Add the agent to the grid.
            self.model.grid.place_agent(child_sheep, self.model.integer_position(child_sheep.x_pos, child_sheep.y_pos))


class Patch(Agent):

    def __init__(self, model, grass_regrowth_time):
        super().__init__(model.next_id(), model)
        # Label the agent as a Sheep.
        self.label = "Patch"

        # Grass regrowth time defines how many steps a patch of dirt will take before growing grass.
        self.grass_regrowth_time = grass_regrowth_time

        # Countdown is used to determine when grass grows back.
        self.countdown = self.model.random.randint(0, grass_regrowth_time)

        # There is a 50% chance upon generation that a patch is grass.
        if self.model.random.uniform(0, 1) < 0.5:
            self.patch_color = DIRT_PATCH
        else:
            self.patch_color = GRASS_PATCH

    def step(self):
        # Grow this patch of grass for every step.
        self.grow()

    def grow(self):
        # If the patch is brown and countdown is not positive, set patch color to green and reset the countdown timer.
        if self.patch_color is DIRT_PATCH and self.countdown <= 0:
            self.patch_color = GRASS_PATCH
            self.countdown = self.grass_regrowth_time

        # Otherwise, decrement the countdown timer by one.
        else:
            self.countdown -= 1


class WolfSheepGrass(Model):

    def __init__(self, width, height, grass_regrowth_rate, initial_wolves, initial_sheep, wolf_food_gain,
                 sheep_food_gain, wolf_reproduction_rate, sheep_reproduction_rate, max_sheep):
        super().__init__()

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
                patch = Patch(self, grass_regrowth_rate)

                # Add the new patch of grass or dirt to its respective scheduler.
                self.patch_schedule.add(patch)

                # Place the patch of grass or dirt at the given coordinate.
                self.grid.place_agent(patch, (x, y))

        # Define DataCollector instance, which tracks the population of wolves and sheep as well as the number of grass.
        get_sheep_count = lambda m: m.sheep_schedule.get_agent_count()
        get_wolf_count  = lambda m: m.wolf_schedule.get_agent_count()
        get_grass_count = lambda m: \
            len([patch for patch in m.patch_schedule.agents if patch.patch_color is GRASS_PATCH]) / 4
        self.dc = DataCollector(model_reporters={"Sheep Count": get_sheep_count,
                                                 "Wolf Count": get_wolf_count,
                                                 "Grass / 4 Count": get_grass_count},
                                                 agent_reporters={})

    def remove(self, agent):
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


    def integer_position(self, x_pos, y_pos):
        return int(x_pos) % self.width, int(y_pos) % self.height

    def print_terrain(self):
        # Print terrain for reference.
        row, col = 0, 0
        patches = []
        for x in range(self.width):
            for y in range(self.height):
                pos = (x, y)
                patch = [agent for agent in self.grid.get_cell_list_contents([pos]) if agent.label == "Patch"][0]
                patches.append(patch)
        for patch in patches:
            if patch.patch_color is GRASS_PATCH:
                print(GREEN_FONT + "🟩", end="")
            else:
                print(BROWN_FONT + "🟩", end="")
            col += 1
            if col == self.width:
                col = 0
                row += 1
                print()
            if row == self.height:
                row = 0
                print(WHITE_FONT)

    def print_population(self, iteration):
        # Print population for reference.
        print("iteration={} wolves={} sheep={} grass={}".format(
            iteration, self.wolf_count, self.sheep_count, self.grass_count))
        print()

    def step(self):
        # After agents have moved, collect sheep, wolf, and grass populations.
        self.dc.collect(self)

        # First, move the sheep.
        self.sheep_schedule.step()

        # Then, move the wolves.
        self.wolf_schedule.step()

        # Finally, grow the grass.
        self.patch_schedule.step()

    def run_model(self):
        iteration = 0  # Keep track of current iteration (remove later)
        self.get_wolf_count()
        self.dc.collect(self)
        # Are the wolves and sheep annihilated?
        are_annihilated = self.wolf_count <= 0 and self.sheep_count <= 0

        # Do the sheep rule the world?
        sheep_inherit = self.wolf_count <= 0 and self.sheep_count > self.max_sheep

        # Continue running the model agents are annihilated or until sheep inherit the earth.
        while not (are_annihilated or sheep_inherit):
            self.print_population(iteration)  # Remove later
            self.print_terrain()  # Remove later

            # Proceed one step or tick.
            self.step()

            iteration += 1

            # Reevaluate stop conditions.
            are_annihilated = self.wolf_count <= 0 and self.sheep_count <= 0
            sheep_inherit = self.wolf_count <= 0 and self.sheep_count > self.max_sheep

        # Print a special message if the sheep inherit the earth.
        if sheep_inherit:
            print("The sheep have inherited the earth.")
        # No message for when sheep and wolves all die out. In either case, end the simulation.
        else:
            pass
