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
		self.interaction_time = 0.001
		self.conversation_time = 0
		self.change_iqr = 0
		self.change_mad = 0
		self.change_speechrate = 0
		self.change_pause = 0
		self.social_sync = 0
		self.activity = 0


	def move_normal(self):
		# examine environment
		possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
		# choose random cells in neighbor grid
		new_position = self.random.choice(possible_steps)
		# move agent to new cell
		self.model.grid.move_agent(self, new_position)

		# get cell-contents
		cell_info = self.model.grid.get_cell_list_contents([self.pos])

		# if the cell contains more than 2 agents already, repeat the movement
		while len(cell_info) > 2:
			# examine environment
			possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
			# choose random cell in new neighbor grid
			new_position = self.random.choice(possible_steps)
			# move the agent
			self.model.grid.move_agent(self, new_position)
			# get new grid info to avoid infinite recursion
			cell_info = self.model.grid.get_cell_list_contents([self.pos])




	# define skeptical move-function
	def move_skeptical(self):
		# examine environment
		possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
		# choose random cells in neighbor grid
		new_position = self.random.choice(possible_steps)
		# move agent to new cell
		self.model.grid.move_agent(self, new_position)

		# get cell-contents
		cell_info = self.model.grid.get_cell_list_contents([self.pos])

		# if the cell contains more than 2 agents already, repeat the movement
		while not len(cell_info) == 1:
			# examine environment
			possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
			# choose random cell in new neighbor grid
			new_position = self.random.choice(possible_steps)
			# move the agent
			self.model.grid.move_agent(self, new_position)
			# get new grid info to avoid infinite recursion
			cell_info = self.model.grid.get_cell_list_contents([self.pos])



    # define step function - what the agent does for each timestep
	def step(self):

		cell = self.model.grid.get_cell_list_contents([self.pos])

		movement_prob = ((0.2 * (1 - self.iqr)) +
						(0.2 * (1 - self.mad)) +
						(0.2 * self.speechrate) +
						(0.2 * (1 - self.pause)) +
						(0.2 * (self.conversation_time / self.interaction_time)))


		if len(cell) == 2:
			other = self.random.choice(cell)
			while other == self:
				other = self.random.choice(cell)
				
			rulebook.linguistic_alignment(self, other)

			rulebook.interaction_time(self, other)
			rulebook.conversation_time(self, other)
			
			rulebook.similarity_check(self, other)

		elif len(cell) != 2:
			rulebook.explore(self, movement_prob)


		if self.status == "Active":
			self.activity += 1
			if movement_prob < float(random.random()):
				self.move_skeptical()
			else:
				self.move_normal()




		print(len(cell))



# defining the model class
class Model(Model):
	# a model-class inheriting the properties of 'Model'
	def __init__(self, N, width, height):
		self.agents = N
		self.grid = MultiGrid(width, height, True)
		self.schedule = RandomActivation(self)
		self.steps = 0
		self.encounters = 0

        # creating agents by iterating through n_agents
		for i in range(self.agents):
        	# specify an agent as an object of class 'Agent' with unique_ID 'i'
			agent = Agent(i, self)

        	# specify pitch measures for the agent as type 'float'
			agent.iqr = float(iqr.iloc[i])
			agent.speechrate = float(speechrate.iloc[i])
			agent.mad = float(mad.iloc[i])
			agent.pause = float(pause.iloc[i])

			agent.symptom_severity = (agent.iqr + agent.mad + (1 - agent.speechrate) + agent.pause) / 4

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
									"change_PauseFreq": "change_pause",
									"social_sync": "social_sync",
									"activity": "activity"},
				model_reporters = {"encounters": "encounters"})

			self.running = True

	def step(self):
		# advance the model and collect data
		self.datacollector.collect(self)
		self.schedule.step()
		self.steps += 1

"""
model = Model(50, 16, 16)
for i in range(100):
	model.step()
	print("Step: {}/499".format(i))
"""
#data = model.datacollector.get_agent_vars_dataframe()
#data.to_csv("data.csv")
#print("CSV written")







	
