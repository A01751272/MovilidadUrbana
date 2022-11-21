from mesa import Model
from mesa.time import StagedActivation
from mesa.space import MultiGrid
from agent import Road, Traffic_Light, Building, Destination, Car
import json
import random


# City model
class CityModel(Model):
    # Initialize variables
    def __init__(self):
        # Web browser configuration
        self.running = True
        # Number of steps
        self.num_steps = 0
        # Declares map dictionary route and reads it
        map_dictionary_file = 'LogicaMultiagentes/map_dictionary.txt'
        map_dictionary = json.load(open(map_dictionary_file))
        # List of available spawn/destination points
        self.parking_coords = []
        # Declares map route
        map_file = 'LogicaMultiagentes/map.txt'

        # Reads the map
        with open(map_file) as map_file:
            # Reading characters by line
            lines = map_file.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)
            # Creates grid and scheduler
            self.grid = MultiGrid(self.width, self.height, torus=False)
            self.schedule = StagedActivation(self, ['step'])

            self.unique_id = 0
            # Adds agents to grid
            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    # Adds road agent
                    if col in ["v", "^", ">", "<", "x"]:
                        agent = Road(f"r{self.unique_id}", self,
                                     map_dictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    # Adds traffic light agent
                    elif col in ["s", "S"]:
                        agent = Traffic_Light(f"t{self.unique_id}", self,
                                              map_dictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                    # Adds building agent
                    elif col == "#":
                        agent = Building(f"b{self.unique_id}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    # Adds destination agent
                    elif col == "e":
                        agent = Destination(f"d{self.unique_id}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.parking_coords.append((c, self.height - r - 1))
                    self.unique_id += 1

        # Add initial cars
        for _ in range(5):
            self.add_car()

    # Adds a agent car to grid and schedule
    def add_car(self):
        # Adds car agent
        destination = random.choice(self.parking_coords)
        # Defines where it starts
        start = random.choice(self.parking_coords)
        # Defines its destination
        agent = Car(f"c{self.unique_id}", self, destination)
        # While they are the same
        while start == destination:
            start = random.choice(self.parking_coords)
        # Adds agent to grid
        self.grid.place_agent(agent, start)
        self.schedule.add(agent)
        self.unique_id += 1

    def step(self):
        # Adds car every 10 seconds
        if self.num_steps % 10 == 0:
            self.add_car()
        '''Advance the model by one step.'''
        self.num_steps += 1
        self.schedule.step()
