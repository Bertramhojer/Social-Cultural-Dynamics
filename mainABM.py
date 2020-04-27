# importing modules
# - mesa modules
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

# matplotlib for plotting when testing
import matplotlib.pyplot as plt
# calculating pseudo-random numbers
import random
# for managing the data-frame produced by the simulation
import pandas as pd

# import dataset
from dataPrep import iqr, mad, pause, speechrate


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

		#self.iqr = 0
		#self.speechrate = 0
		#self.mad = 0
		#self.pause = 0

		# specify agent-properties
		self.sociality = 0
		self.alignment = 0

	# define function for moving around the environment
	def move(self):
		possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
		new_position = self.random.choice(possible_steps)
		self.model.grid.move_agent(self, new_position)

    # defining functions for rule-based interaction
    # rule based on iqr
	def ruleOne(self):
    	# check the neighbourhood for agents
		cellmates = self.model.grid.get_cell_list_contents([self.pos])
    	# specify other based on amount of agents in the cell
		other = self.random.choice(cellmates)

        # interaction rule
		if self.iqr < other.iqr:
			self.alignment += 0.1
			other.alignment -= 0.1

    # rule based on rate
	def ruleTwo(self):
    	# check the neighbourhood for agents
		cellmates = self.model.grid.get_cell_list_contents([self.pos])
    	# specify other based on amount of agents in the cell
		other = self.random.choice(cellmates)

        # interaction rule
		if self.speechrate > other.speechrate:
			self.sociality += 0.1
			other.sociality -= 0.1

    # define step function - what the agent does for each timestep
	def step(self):
		self.move()
		self.ruleOne()
		self.ruleTwo()
		# print("Current sociality {}".format(self.sociality))
		# print("Current alignment {}".format(self.alignment))



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
				agent_reporters = {"Variability": "iqr",
									"Speechrate": "speechrate",
									"MAD": "mad",
									"PauseFreq": "pause",
									"Alignment": "alignment",
									"Sociality": "sociality"})

	def step(self):
		# advance the model and collect data
		self.datacollector.collect(self)
		self.schedule.step()

model = Model(50, 10, 10)
for i in range(10):
	model.step()

data = model.datacollector.get_agent_vars_dataframe()
data.to_csv("asdABM.csv")
print("CSV written")







	
