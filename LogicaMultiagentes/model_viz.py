from model import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer


# Agent portrayal
def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red",
                 "r": 0.5}

    # Colors agents based on types
    if agent.type == 'car':
        portrayal["Color"] = "red"
        portrayal["text"] = agent.unique_id
    elif agent.type == 'road':
        portrayal["Color"] = "grey"
        portrayal["r"] = 0.1
    elif agent.type == 'light':
        if agent.state:
            portrayal["Color"] = "green"
        else:
            portrayal["Color"] = "red"
    elif agent.type == 'parking':
        portrayal["Color"] = "blue"
    elif agent.type == 'building':
        portrayal["Color"] = "grey"
    return portrayal


# Get width and height from map
with open('LogicaMultiagentes/map.txt') as map_file:
    lines = map_file.readlines()
    width = len(lines[0])-1
    height = len(lines)

# Run model
grid = CanvasGrid(agent_portrayal, width, height, 750, 750)
server = ModularServer(CityModel,
                       [grid],
                       "City Model")
server.port = 8521
server.launch()
