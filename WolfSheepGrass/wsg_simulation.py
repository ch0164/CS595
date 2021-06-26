from wsg_visualization import *  # Import the server used to run the simulation.

# Set width and length of the world. NetLogo default is 51x51.
world_width, world_length = 51, 51

if __name__ == "__main__":
    run_server(world_width, world_length)
