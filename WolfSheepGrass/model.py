from Utilities.common_imports import *
from Utilities.constants import *
from mesa.space import ContinuousSpace, SingleGrid
from mesa import Agent, Model
from mesa.time import RandomActivation


class Wolf(Agent):

    def __init__(self, unique_id, model, pos, food_gain, reproduction_rate):
        super().__init__(unique_id, model)
        self.x, self.y = pos
        self.food_gain, self.reproduction_rate = food_gain, reproduction_rate
        self.energy = 2 * random.randrange(0, food_gain)
        self.label = "Wolf"

    def step(self):
        self.move()
        self.energy -= 1
        self.eat()
        if self.energy <= 0:
            self.model.wolf_schedule.remove(self)
        self.reproduce()

    def move(self):
        # TODO: How should the agent rotate and move?

        self.x += random.random()
        self.y += 1 - self.x
        self.model.grid.move_agent(self, (self.x, self.y))

    def eat(self):
        # Eat sheep which share the same patch
        int_pos = (int(self.x) % self.model.width, int(self.y) % self.model.height)
        sheep_list = [agent.label == "Sheep" for agent in self.model.grid.get_neighbors(int_pos, 1)]
        if sheep_list:
            sheep = sheep_list[0]  # Eat the first sheep found
            self.model.remove(sheep)
            self.energy += self.food_gain

    def reproduce(self):
        pass


class Sheep(Agent):

    def __init__(self, unique_id, model, pos, food_gain, reproduction_rate):
        super().__init__(unique_id, model)
        self.x, self.y = pos
        self.food_gain, self.reproduction_rate = food_gain, reproduction_rate
        self.energy = 2 * random.randrange(0, food_gain)
        self.label = "Sheep"

    def step(self):
        self.move()
        self.energy -= 1
        self.eat()
        if self.energy <= 0:
            self.model.remove(self)
        self.reproduce()

    def move(self):
        # Need to work on how to "turn".

        self.x += random.random()
        self.y += 1 - self.x
        self.model.grid.move_agent(self, (self.x, self.y))

    def eat(self):
        int_pos = (int(self.x) % self.model.width, int(self.y) % self.model.height)
        patch = self.model.terrain.get_cell_list_contents([int_pos])[0]
        if patch.patch_color is GRASS_PATCH:
            patch.patch_color = DIRT_PATCH
            self.energy += self.food_gain
            self.model.grass_count -= 1

    def reproduce(self):
        if random.random() < self.reproduction_rate:
            self.energy /= 2
            child_sheep = self.breed(self.energy, (self.x, self.y))  # Deep copy is really slow
            # TODO: Rotate and move the child 1 unit.
            if random.random() < 0.5:
                child_sheep.x -= 1
            else:
                child_sheep.x += 1
            if random.random() < 0.5:
                child_sheep.y -= 1
            else:
                child_sheep.y += 1
            self.model.sheep_schedule.add(child_sheep)
            self.model.grid.place_agent(child_sheep, (child_sheep.x, child_sheep.y))
            self.model.sheep_count += 1

    def breed(self, energy, pos):
        child = Sheep(self.model.id, self.model, pos, self.food_gain, self.reproduction_rate)
        self.energy = energy
        self.model.id += 1
        return child


class Patch(Agent):

    def __init__(self, unique_id, model, grass_regrowth_time):
        super().__init__(unique_id, model)
        self.grass_regrowth_time = grass_regrowth_time
        self.countdown = random.randrange(0, grass_regrowth_time)
        self.label = "Patch"

        # There is a 50% chance upon generation that a patch is grass.
        if random.random() < 0.5:
            self.patch_color = DIRT_PATCH
        else:
            self.patch_color = GRASS_PATCH

    def step(self):
        self.grow()

    def grow(self):
        # If the patch is brown and countdown is not positive, set patch color to green and reset the countdown timer.
        if self.patch_color is DIRT_PATCH and self.countdown <= 0:
            self.patch_color = GRASS_PATCH
            self.countdown = self.grass_regrowth_time
            self.model.grass_count += 1

        # Otherwise, decrement the countdown timer by one.
        else:
            self.countdown -= 1


class WolfSheepGrass(Model):

    def __init__(self, width, height, grass_regrowth_rate, initial_wolves, initial_sheep, wolf_food_gain,
                 sheep_food_gain, wolf_reproduction_rate, sheep_reproduction_rate, max_sheep):
        super().__init__()
        self.width, self.height = width, height
        self.wolf_count, self.sheep_count = initial_wolves, initial_sheep
        self.grass_count = 0
        self.agent_count = initial_wolves + initial_sheep
        self.max_sheep = max_sheep
        self.id = 1  # ID unique to each agent in the simulation
        # Instantiate continuous, toroidal grid for movement of wolves and sheep.
        self.grid = ContinuousSpace(width, height, True)
        # Instantiate discrete, toroidal grid for patches of grass and dirt.
        self.terrain = SingleGrid(width, height, True)
        # Initialize the scheduler, which activates agents in a random order per step/tick.
        self.sheep_schedule = RandomActivation(self)  # Equivalent to Netlogo "ask agents"
        self.wolf_schedule = RandomActivation(self)
        self.patch_schedule = RandomActivation(self)
        # Add agents to the model.
        # Add initial sheep (they move first in the NetLogo simulation).
        for _ in range(initial_sheep):
            x = self.random.random() * width
            y = self.random.random() * height
            pos = (x, y)
            sheep = Sheep(self.id, self, pos, sheep_food_gain, sheep_reproduction_rate)
            self.id += 1
            self.sheep_schedule.add(sheep)
            self.grid.place_agent(sheep, pos)
        # Add initial wolves.
        for _ in range(initial_wolves):
            x = self.random.random() * width
            y = self.random.random() * height
            pos = (x, y)
            wolf = Wolf(self.id, self, pos, wolf_food_gain, wolf_reproduction_rate)
            self.wolf_schedule.add(wolf)
            self.id += 1
            self.grid.place_agent(wolf, pos)
        # Initialize environment.
        for y in range(height):
            for x in range(width):
                patch = Patch(self.id, self, grass_regrowth_rate)
                if patch.patch_color is GRASS_PATCH:
                    self.grass_count += 1
                self.patch_schedule.add(patch)
                self.id += 1
                self.terrain.place_agent(patch, (x, y))

    def remove(self, agent):
        # Remove agent from simulation.
        if agent.label == "Wolf":
            self.wolf_schedule.remove(agent)
            self.grid.remove_agent(agent)
            self.wolf_count -= 1
        elif agent.label == "Sheep":
            self.sheep_schedule.remove(agent)
            self.grid.remove_agent(agent)
            self.sheep_count -= 1
        elif agent.label == "Patch":
            pass

    def print_terrain(self):
        row, col = 0, 0
        for patch in self.terrain:
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
        self.wolf_schedule.step()   # Move the wolves,
        self.sheep_schedule.step()  # and sheep,
        self.patch_schedule.step()  # and grow grass.

    def run_model(self):
        # Continue running the model agents are annihilated or until sheep inherit the earth.
        iteration = 0
        are_annihilated = self.wolf_count <= 0 and self.sheep_count <= 0
        sheep_inherit = self.wolf_count <= 0 and self.sheep_count > self.max_sheep
        while not (are_annihilated or sheep_inherit):
            self.step()
            self.print_population(iteration)
            self.print_terrain()
            iteration += 1
            are_annihilated = self.wolf_count <= 0 and self.sheep_count <= 0
            sheep_inherit = self.wolf_count <= 0 and self.sheep_count > self.max_sheep
        if are_annihilated:
            pass  # No message for this
        else:
            print("The sheep have inherited the earth.")
