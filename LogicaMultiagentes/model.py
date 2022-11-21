from mesa import Model
from mesa.time import StagedActivation
from mesa.space import MultiGrid
from agent import Road, Traffic_Light, Building, Destination, Car
import json
import random


# City model
class CityModel(Model):
    def __init__(self):
        # TODO change route
        map_dictionry_file = 'LogicaMultiagentes/map_dictionary.txt'
        # Reads the dictionary of agent terms
        map_dictionary = json.load(open(map_dictionry_file))
        # List of available spawn/destination points
        parking_coords = []

        # TODO change route
        map_file = 'LogicaMultiagentes/map.txt'
        # Reads the map
        with open(map_file) as map_file:
            lines = map_file.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)

            # Creates grid and scheduler
            self.grid = MultiGrid(self.width, self.height, torus=False)
            # TODO Change list of steps
            self.schedule = StagedActivation(self, ['step'])

            # Adds agents to grid
            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    # Adds road agent
                    if col in ["v", "^", ">", "<", "x"]:
                        agent = Road(f"r{r*self.width+c}", self,
                                     map_dictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    # Adds traffic light agent
                    elif col in ["s", "S"]:
                        agent = Traffic_Light(f"tl{r*self.width+c}", self,
                                              map_dictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                    # Adds building agent
                    elif col == "#":
                        agent = Building(f"ob{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    # Adds destination agent
                    elif col == "e":
                        agent = Destination(f"d{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        parking_coords.append((c, self.height - r - 1))
        self.running = True

        # Add car (Test)
        fin = random.choice(parking_coords)
        start = random.choice(parking_coords)
        agent = Car(f"r{r*self.width+c}", self, fin)
        while start == fin:
            start = random.choice(parking_coords)
        self.grid.place_agent(agent, start)
        self.schedule.add(agent)

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
