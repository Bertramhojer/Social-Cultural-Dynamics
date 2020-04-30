from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from mainABM import *


# potential text-module class

def agent_portrayal(agent):
	portrayal = {"Shape": "circle",
				"Filled": "true",
				"r": 0.5}



	if agent.unique_interactions <= 5:
		portrayal["Color"] = "red"
		portrayal["Layer"] = 0
	elif agent.unique_interactions > 5:
		portrayal["Color"] = "blue"
		portrayal["Layer"] = 1
		portrayal["r"] = 0.4
		if agent.unique_interactions > 10:
			portrayal["Color"] = "green"
			portrayal["Layer"] = 2
			portrayal["r"] = 0.3

	return portrayal


grid = CanvasGrid(agent_portrayal, 16, 16, 500, 500)

server = ModularServer(Model,
                       [grid],
                       "Social Interaction Model",
                       {"N":50, "width":16, "height":16})
server.port = 8521 # The default
server.launch()