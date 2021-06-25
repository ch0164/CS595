from wsg_model import WolfSheepGrass                               # The WolfSheepGrass model
from mesa.visualization.modules import CanvasGrid, ChartModule     # Type of grid to visualize agents
from mesa.visualization.ModularVisualization import ModularServer  # Creates the new server to host the model
from mesa.visualization.UserParam import UserSettableParameter     # Allows UI elements like sliders

GRASS_PATCH = True
DIRT_PATCH = False

def agent_portrayal(agent):
    # Set up portrayal dictionary which stores attributes of the agent.
    portrayal = {"Filled" : "true"}

    # Is the agent a patch?
    if agent.label == "Patch":
        # Fill the entire cell. Patches are displayed on the bottom layer.
        portrayal["Shape"], portrayal["w"], portrayal["h"], portrayal["Layer"] = "rect", 1, 1, 0

        # Is the patch grass or dirt?
        if agent.patch_color is GRASS_PATCH:
            portrayal["Color"] = "green"
        else:
            portrayal["Color"] = "#A0522D"  # Color code for brown

    # Is the agent a sheep?
    elif agent.label == "Sheep":
        # Sheep are displayed above patches and below wolves as white circles.
        portrayal["Shape"], portrayal["r"], portrayal["Color"], portrayal["Layer"] = "circle", 0.5, "white", 1
        if agent.just_spawned:
            portrayal["Color"] = "blue"
            agent.just_spawned = False
        elif agent.energy < 5:
            portrayal["Color"] = "red"

    # Is the agent a wolf?
    elif agent.label == "Wolf":
        # Wolves are displayed above patches and sheep as black squares.
        portrayal["Shape"], portrayal["w"], portrayal["h"] = "rect", 0.5, 0.5
        portrayal["Color"], portrayal["Layer"] = "black", 2
        if agent.just_spawned:
            portrayal["Color"] = "blue"
            agent.just_spawned = False
        elif agent.energy < 5:
            portrayal["Color"] = "red"

    return portrayal


def run_server(world_width, world_height):
    grid = CanvasGrid(agent_portrayal, world_width, world_height, 700, 700)
    population_dicts = [dict(Label="Sheep Count", Color="blue"),
                        dict(Label="Wolf Count", Color="red"),
                        dict(Label="Grass / 5 Count", Color="green")]
    population_chart = ChartModule(population_dicts, data_collector_name="dc")

    number_of_wolves_slider = UserSettableParameter(
        "slider", "initial-number-wolves", 50, 0, 250, 1)
    number_of_sheep_slider = UserSettableParameter(
        "slider", "initial-number-sheep", 100, 0, 250, 1)
    grass_regrowth_time = UserSettableParameter(
        "slider", "grass-regrowth-time", 30, 0, 100, 1)
    sheep_food_gain = UserSettableParameter(
        "slider", "sheep-gain-from-food", 4, 0, 50, 1)
    wolf_food_gain = UserSettableParameter(
        "slider", "wolf-gain-from-food", 20, 0, 100, 1)
    sheep_reproduce = UserSettableParameter(
        "slider", "sheep-reproduce", 0.04, 0.01, 0.20, 0.01)
    wolf_reproduce = UserSettableParameter(
        "slider", "wolf-reproduce", 0.05, 0.00, 0.20, 0.01)

    server = ModularServer(WolfSheepGrass,
                           [grid, population_chart],
                           "Wolf-Sheep-Grass Model",
                           {"width" : world_width, "height" : world_height,
                            "grass_regrowth_rate" : grass_regrowth_time,
                            "initial_wolves" : number_of_wolves_slider, "initial_sheep" : number_of_sheep_slider,
                            "wolf_food_gain" : wolf_food_gain, "sheep_food_gain" : sheep_food_gain,
                           "wolf_reproduction_rate" : wolf_reproduce, "sheep_reproduction_rate" : sheep_reproduce,
                            "max_sheep" : 10_000})
    server.port = 8521
    server.launch()