from movilidad_urbana import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red",
                 "r": 0.5}
    if agent.color == 1:
        portrayal["Color"] = "green"
    return portrayal


grid = CanvasGrid(agent_portrayal, 28, 28, 750, 750)
server = ModularServer(MovilidadUrbana,
                       [grid],
                       "Dirty Cleaner Model",
                       {"width": 28,
                        "height": 28})
server.port = 8521  # Default port
server.launch()
