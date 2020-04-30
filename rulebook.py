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
# data handling
import numpy as np
# for creating binomial distributions aiding decision-making
from scipy.stats import binom
import math



# checking whether the agents are similar and estimating a probability of moving to a new grid
def similarity_check(agent, other):
    iqr_diff = np.absolute(agent.iqr - other.iqr)
    mad_diff = np.absolute(agent.mad - other.mad)
    speechrate_diff = np.absolute(agent.speechrate - other.speechrate)
    pause_diff = np.absolute(agent.pause - other.pause)

    # probability of moving
    movement_prob = ((0.125 * agent.iqr + 0.125 * iqr_diff) + 
                    (0.125 * agent.mad + 0.125 * mad_diff) +
                    (0.125 * (1 - agent.speechrate) + 0.125 * speechrate_diff) +
                    (0.125 * agent.pause + 0.125 * pause_diff))

    rand_n = float(random.random())
    if movement_prob > rand_n:
        agent.status = "Active"
    else:
        agent.status = "Inactive"
    #print(agent.status)
    #print(movement_prob)


# If alone on a cell, set status to active with probability based on pitch-scores
def explore(agent):
    # probability of moving
    movement_prob = ((0.25 * (1 - agent.iqr)) + 
                    (0.25 * (1 - agent.mad)) +
                    (0.25 * agent.speechrate) +
                    (0.25 * (1 - agent.pause)))

    rand_n = float(random.random())
    if movement_prob > rand_n:
        agent.status = "Active"
    else:
        agent.status = "Inactive"


# Counting the amount of time an agent has interacted
def interaction_time(agent, other):
    cell_info = agent.model.grid.get_cell_list_contents([agent.pos])
    if len(cell_info) == 2:
        agent.interaction_time += 1
        if agent.status == "Active" or other.status == "Active":
            agent.unique_interactions += 1


# Counting conversation time
def conversation_time(agent, other):
    # calculating the ratio between agents pause frequency
    agent.conversation_time += agent.pause / (agent.pause + other.pause)


# Linguistic alignment
def linguistic_alignment(agent, other):
    # calculate social synchronisation score based on pitch scores
    social_sync = ((0.1 * (1 - agent.iqr)) + 
                    (0.1 * (1 - agent.mad)) +
                    (0.1 * agent.speechrate) +
                    (0.1 * (1 - agent.pause)))

    # calculate the difference between agents
    iqr_diff = agent.iqr - other.iqr
    mad_diff = agent.mad - other.mad
    speechrate_diff = agent.speechrate - other.speechrate
    pause_diff = agent.pause - other.pause

    # modulate based on second degree polynomium
    agent.change_iqr += (social_sync * (-1 * (math.pow(iqr_diff, 2) + 1))) * iqr_diff
    agent.change_mad += (social_sync * (-1 * (math.pow(mad_diff, 2) + 1))) * mad_diff
    agent.change_speechrate += (social_sync * (-1 * (math.pow(speechrate_diff, 2) + 1))) * speechrate_diff
    agent.change_pause += (social_sync * (-1 * (math.pow(pause_diff, 2) + 1))) * pause_diff



# 




