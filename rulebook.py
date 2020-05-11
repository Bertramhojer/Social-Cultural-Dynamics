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
import math



# checking whether the agents are similar and estimating a probability of moving to a new grid
def similarity_check(agent, other):
    iqr_diff = np.absolute(agent.iqr - other.iqr)
    mad_diff = np.absolute(agent.mad - other.mad)
    speechrate_diff = np.absolute(agent.speechrate - other.speechrate)
    pause_diff = np.absolute(agent.pause - other.pause)


    diff = (iqr_diff + mad_diff + speechrate_diff + pause_diff) / 4
    # self weight
    self_weight = 0.4 * diff + 0.03
    # diff weight
    diff_weight = agent.symptom_severity * diff + 0.03


    # probability of moving
    activation_prob = ((self_weight * agent.iqr + diff_weight * iqr_diff) + 
                    (self_weight * agent.mad + diff_weight * mad_diff) +
                    (self_weight * (1 - agent.speechrate) + diff_weight * speechrate_diff) +
                    (self_weight * agent.pause + diff_weight * pause_diff))

    rand_n = float(random.random())
    if activation_prob > rand_n:
        agent.status = "Active"
    else:
        agent.status = "Inactive"


# If alone on a cell, set status to active with probability based on pitch-scores
def explore(agent, movement_prob):
    # setting status based on movement_prob as defined in the step-function()
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
    iqr_sync = 0.7 * (1 - agent.iqr)
    mad_sync = 0.7 * (1 - agent.mad)
    speechrate_sync = 0.7 * agent.speechrate
    pause_sync = 0.7 * (1 - agent.pause)

    # calculate the difference between agents
    iqr_diff = other.iqr - agent.iqr
    mad_diff = other.mad - agent.mad
    speechrate_diff = other.speechrate - agent.speechrate
    pause_diff = other.pause - agent.pause

    # modulate based on second degree polynomium
    agent.change_iqr += (iqr_sync * (-1 * (iqr_diff * iqr_diff) + 1)) * iqr_diff
    agent.change_mad += (mad_sync * (-1 * (mad_diff * mad_diff) + 1)) * mad_diff
    agent.change_speechrate += (speechrate_sync * (-1 * (speechrate_diff * speechrate_diff) + 1)) * speechrate_diff
    agent.change_pause += (pause_sync * (-1 * (pause_diff * pause_diff) + 1)) * pause_diff

    # calculate absolute change
    agent.abs_change_iqr += np.absolute((iqr_sync * (-1 * (iqr_diff * iqr_diff) + 1)) * iqr_diff)
    agent.abs_change_mad += np.absolute((mad_sync * (-1 * (mad_diff * mad_diff) + 1)) * mad_diff)
    agent.abs_change_speechrate += np.absolute((speechrate_sync * (-1 * (speechrate_diff * speechrate_diff) + 1)) * speechrate_diff)
    agent.abs_change_pause += np.absolute((pause_sync * (-1 * (pause_diff * pause_diff) + 1)) * pause_diff)


