
from model import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red",
                 "r": 0.5}

    if agent.color == 'car':
        portrayal["Color"] = "red"
    elif agent.color == 'road':
        portrayal["Color"] = "grey"
        portrayal["r"] = 0.1
    elif agent.color == 'light':
        portrayal["Color"] = "green"
    elif agent.color == 'park':
        portrayal["Color"] = "blue"
    elif agent.color == 'building':
        portrayal["Color"] = "grey"

    return portrayal


with open('LogicaMultiagentes/map.txt') as map_file:
    lines = map_file.readlines()
    width = len(lines[0])-1
    height = len(lines)

N = 30
grid = CanvasGrid(agent_portrayal, width, height, 750, 750)
server = ModularServer(CityModel,
                       [grid],
                       "City Model",
                       {"N": N})
server.port = 8521
server.launch()
