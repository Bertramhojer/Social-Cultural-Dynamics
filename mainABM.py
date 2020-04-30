# importing modules
# - mesa modules
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid, Grid
from mesa.datacollection import DataCollector

# matplotlib for plotting when testing
import matplotlib.pyplot as plt
# calculating pseudo-random numbers
import random
# for managing the data-frame produced by the simulation
import pandas as pd
# data handling
import numpy as np

# import dataset
from dataPrep import iqr, mad, pause, speechrate

# import interaction rules
import rulebook


# defining the agent class
class Agent(Agent):
	# An agent-cass inheriting the properties of Agent
	# define properties needed to specify an object of class Agent()
	def __init__(self, unique_id, model):
		super().__init__(unique_id, model)
		# specify pitch measures for the agent
		""" Perhaps we don't need to specify the values that are initiated by the dataframe, we do however have
		to specify any variables that we make up that are manipulated by interaction rules. So if an initial 
		value is manipulated over time we have to specify that in the start a well. """

		# specify activity-level
		self.status = "Active"

		# specify agent-properties
		self.unique_interactions = 0
		self.interaction_time = 0
		self.conversation_time = 0
		self.change_iqr = 0
		self.change_mad = 0
		self.change_speechrate = 0
		self.change_pause = 0

	
	def move(self):
		# examine environment
		possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
		# choose random cells in neighbor grid
		new_position = self.random.choice(possible_steps)
		# move agent to new cell
		self.model.grid.move_agent(self, new_position)

		# get cell-contents
		cell_info = self.model.grid.get_cell_list_contents([self.pos])

		# if the cell contains more than 2 agents already, repeat the movement
		while len(cell_info) > 1:
			# examine environment
			possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
			# choose random cell in new neighbor grid
			new_position = self.random.choice(possible_steps)
			# get new grid info to avoid infinite recursion
			cell_info = self.model.grid.get_cell_list_contents([self.pos])
			# move the agent
			self.model.grid.move_agent(self, new_position)



    # define step function - what the agent does for each timestep
	def step(self):

		cell = self.model.grid.get_cell_list_contents([self.pos])
		
		if len(cell) == 2:
			other = self.random.choice(cell)
			while other == self:
				other = self.random.choice(cell)
				
			rulebook.linguistic_alignment(self, other)

			rulebook.interaction_time(self, other)
			rulebook.conversation_time(self, other)
			
			rulebook.similarity_check(agent = self, other = other)

			#print(other.iqr)
			#print(self.iqr)

		elif len(cell) != 2:
			rulebook.explore(self)


		if self.status == "Active":
			self.move()



# defining the agent class
class Model(Model):
	# a model-class inheriting the properties of 'Model'
	def __init__(self, N, width, height):
		self.agents = N
		self.grid = MultiGrid(width, height, True)
		self.schedule = RandomActivation(self)

        # creating agents by iterating through n_agents
		for i in range(self.agents):
        	# specify an agent as an object of class 'Agent' with unique_ID 'i'
			agent = Agent(i, self)

        	# specify pitch measures for the agent as type 'float'
			agent.iqr = float(iqr.iloc[i])
			agent.speechrate = float(speechrate.iloc[i])
			agent.mad = float(mad.iloc[i])
			agent.pause = float(pause.iloc[i])

        	# add the agent to the model schedule
			self.schedule.add(agent)

        	# adding the agent to a random grid cell
			x = self.random.randrange(self.grid.width)
			y = self.random.randrange(self.grid.height)
			self.grid.place_agent(agent, (x, y))

			# add data-collector to the agent
			self.datacollector = DataCollector(
				agent_reporters = {"interactions": "unique_interactions",
									"interaction_time": "interaction_time",
									"conversation_time": "conversation_time",
									"change_IQR": "change_iqr",
									"change_MAD": "change_mad",
									"change_Speechrate": "change_speechrate",
									"change_PauseFreq": "change_pause"})

	def step(self):
		# advance the model and collect data
		self.datacollector.collect(self)
		self.schedule.step()

model = Model(50, 10, 10)
for i in range(200):
	model.step()
	print("Step: {}/199".format(i))

data = model.datacollector.get_agent_vars_dataframe()
data.to_csv("data.csv")
print("CSV written")







	
