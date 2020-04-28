# importing modules
# - mesa modules
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

# calculating pseudo-random numbers
import random
# for managing the data-frame produced by the simulation
import pandas as pd


def rule_one():