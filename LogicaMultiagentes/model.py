from mesa import Model
from mesa.time import StagedActivation
from mesa.space import MultiGrid
# from agent import *
import json


class CityModel(Model):
    def __init__(self, N):
        map_dictionary = json.load(open("map_dictionary.txt"))

        with open('map.txt') as map_file:
            lines = map_file.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)

            self.grid = MultiGrid(self.width, self.height, torus=False)
            self.schedule = StagedActivation(self)

            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    if col in ["v", "^", ">", "<", "x"]:
                        agent = Road(f"r{r*self.width+c}", self,
                                     map_dictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    elif col in ["s"]:
                        agent = Traffic_Light(f"tl{r*self.width+c}", self,
                                              False if col == "S" else True,
                                              int(map_dictionary[col]))
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                    elif col == "#":
                        agent = Obstacle(f"ob{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    elif col == "e":
                        agent = Destination(f"d{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))

        self.num_agents = N
        self.running = True

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        if self.schedule.steps % 10 == 0:
            for agents, x, y in self.grid.coord_iter():
                for agent in agents:
                    if isinstance(agent, Traffic_Light):
                        agent.state = not agent.state