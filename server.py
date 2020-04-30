from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule, TextElement

from mainABM import *


# define class for counting steps
class StepElement(TextElement):
	def __init__(self):
		pass

	def render(self, model):
		return "Number of steps: " + str(model.steps)

# set steps equal to the specified class
steps = StepElement()

# define function for specifying agent-representation
def agent_portrayal(agent):
	portrayal = {"Shape": "circle",
				"Filled": "true",
				"interactions": agent.unique_interactions,
				"conversation time": round(agent.conversation_time, 3),
				"symptom severity": round(agent.symptom_severity, 3),
				"moves": agent.activity,
				"r": 0.5}

	if agent.unique_interactions > 10:
		portrayal["Color"] = "green"
		portrayal["Layer"] = 2
		portrayal["r"] = 0.3

	elif agent.unique_interactions > 5:
		portrayal["Color"] = "blue"
		portrayal["Layer"] = 1
		portrayal["r"] = 0.4

	elif agent.unique_interactions <= 5:
		portrayal["Color"] = "red"
		portrayal["Layer"] = 0

	return portrayal


# specify the grid with dimensions equal to model-dimensions
grid = CanvasGrid(agent_portrayal, 16, 16, 500, 500)

# specify server-value of class ModularServer (MESA)
server = ModularServer(Model,
                       [grid, steps],
                       "Social Interaction Model",
                       {"N":50, "width":16, "height":16})
server.port = 8521 # The default

# run the server using the server-class' 'launch' function
server.launch()