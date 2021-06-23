from wsg_model import WolfSheepGrass                               # The WolfSheepGrass model
from mesa.visualization.modules import CanvasGrid                  # Type of grid to visualize agents
from mesa.visualization.ModularVisualization import ModularServer  # Creates the new server to host the model
from mesa.visualization.UserParam import UserSettableParameter     # Allows UI elements like sliders

# TODO: Might need to create a visualization module to support ContinuousSpace (CanvasGrid only works for Grids)
def agent_portrayal(agent):
    # Set up portrayal dictionary which stores attributes of the agent.
    portrayal = {"Shape" : "circle",  # Agent shape
                 "Filled" : "true",   # Fill shape
                 "r" : 0.5}           # Radius
    return portrayal


def run_server():
    grid = CanvasGrid(agent_portrayal, 50, 50, 500, 500)
    server = ModularServer(WolfSheepGrass,
                           [grid],
                           "Wolf-Sheep-Grass Model",
                           {"width" : 50, "height" : 50,
                            "grass_regrowth_rate" : 30, "initial_wolves" : 50, "initial_sheep" : 100,
                            "wolf_food_gain" : 20, "sheep_food_gain" : 4,
                           "wolf_reproduction_rate" : 0.05, "sheep_reproduction_rate" : 0.04,
                            "max_sheep" : 10_000})
    server.port = 8521
    server.launch()