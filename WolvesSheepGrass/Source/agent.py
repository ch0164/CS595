"""

Title:          Agent

Description:    The objective of this file is to contain class definitions for this project's two agents,
                wolves and sheep.

"""

# Project Related Imports
from Utilities.common_imports import *
from Utilities.constants import *

# Global Variable Declarations

# IDE Likes Two Empty Lines Before Class Definition


class Agent:

    def __init__(self):
        self.symbol = ""


class Wolf(Agent):

    def __init__(self):
        Agent.__init__(self)
        self.symbol = "x"


class Sheep(Agent):

    def __init__(self):
        Agent.__init__(self)
        self.symbol = "o"
        pass


# IDE Likes Empty Line At End Of File
