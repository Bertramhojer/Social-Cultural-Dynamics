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


chart = ChartModule([{"Label": "encounters",
					"Color": "blue"}],
					data_collector_name = 'datacollector')

# set steps equal to the specified class
steps = StepElement()

# define function for specifying agent-representation
def agent_portrayal(agent):
	if len(agent.model.grid.get_cell_list_contents([agent.pos])) == 1:
		portrayal = {"Shape": "circle",
					"Filled": "true",
					"interactions": agent.unique_interactions,
					"conversation time": round(agent.conversation_time, 3),
					"interaction time": round(agent.interaction_time, 3),
					"symptom severity": round(agent.symptom_severity, 3),
					"moves": agent.activity}

		if agent.unique_interactions > 10:
			portrayal["Color"] = "green"
			portrayal["Layer"] = 1
			portrayal["r"] = 0.3

		elif agent.unique_interactions > 5:
			portrayal["Color"] = "blue"
			portrayal["Layer"] = 1
			portrayal["r"] = 0.5

		elif agent.unique_interactions <= 5:
			portrayal["Color"] = "red"
			portrayal["Layer"] = 1
			portrayal["r"] = 0.7

	elif len(agent.model.grid.get_cell_list_contents([agent.pos])) == 2:
		portrayal = {"Shape": "rect",
					"Filled": "true",
					"interactions": agent.unique_interactions,
					"conversation time": round(agent.conversation_time, 3),
					"interaction time": round(agent.interaction_time, 3),
					"symptom severity": round(agent.symptom_severity, 3),
					"moves": agent.activity}

		if agent.unique_interactions > 10:
			portrayal["Color"] = "green"
			portrayal["Layer"] = 1
			portrayal["w"] = 0.3
			portrayal["h"] = 0.3

		elif agent.unique_interactions > 5:
			portrayal["Color"] = "blue"
			portrayal["Layer"] = 1
			portrayal["w"] = 0.5
			portrayal["h"] = 0.5

		elif agent.unique_interactions <= 5:
			portrayal["Color"] = "red"
			portrayal["Layer"] = 1
			portrayal["w"] = 0.7
			portrayal["h"] = 0.7

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