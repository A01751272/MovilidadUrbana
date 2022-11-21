from mesa import Model
from mesa.time import StagedActivation
from mesa.space import MultiGrid
from agent import *
import json


class CityModel(Model):
    def __init__(self, N):
        map_dictionary = json.load(open('LogicaMultiagentes/\
            map_dictionary.txt'))

        with open('LogicaMultiagentes/map.txt') as map_file:
            lines = map_file.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)

            self.grid = MultiGrid(self.width, self.height, torus=False)
            self.schedule = StagedActivation(self, ['step'])

            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    if col in ["v", "^", ">", "<", "x"]:
                        agent = Road(f"r{r*self.width+c}", self,
                                     map_dictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    elif col == "s":
                        agent = Traffic_Light(f"tl{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                    elif col == "#":
                        agent = Building(f"ob{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    elif col == "e":
                        agent = Destination(f"d{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))

        self.num_agents = N
        self.running = True

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
