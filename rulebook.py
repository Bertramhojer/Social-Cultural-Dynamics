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
# for creating binomial distributions aiding decision-making
from scipy.stats import binom
# plotting
import matplotlib.pyplot as plt



def similarity_check(current_agent, other_agent):
    if abs(other_overall-self_overall) <= 0.5:
        if binom.rvs(n = 1, p = 0.3) == 1:
            self.status = "Inactive"
            self.conversation_time += 1
        else: 
            self.status = "Active"




def rule_one():
    # get info on other agents in the cell
    cellmates = self.model.grid.get_cell_list_contents([self.pos])
    # if there are more than one agent choose either one of them
    other = self.random.choice(cellmates)
    # run similarity check
    similarity_check(current_agent = self, other_agent = other)