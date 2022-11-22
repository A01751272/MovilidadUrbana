from mesa import Model
from mesa.time import StagedActivation
from mesa.space import MultiGrid
from astar import Astar
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
        # Reserved cells
        self.reserved_cells = {}
        self.car_occupied = {}

        # Reads the map
        with open(map_file) as map_file:
            # Reading characters by line
            lines = map_file.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)
            # Creates grid and scheduler
            self.grid = MultiGrid(self.width, self.height, torus=False)
            self.schedule = StagedActivation(self, ['step', 'step2', 'step3'])

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
        # for _ in range(5):
        #     self.add_car()

        # Coche manejando (Test)
        # agent = Car(f"c{1001}", self, (18, 20))
        # agent.priority = 1
        # agent.cant_move = False
        # self.grid.place_agent(agent, (17, 9))
        # self.schedule.add(agent)
        # Segundo coche manejando (Test)
        # agent = Car(f"c{1002}", self, (18, 20))
        # agent.priority = 1
        # agent.cant_move = False
        # self.grid.place_agent(agent, (17, 8))
        # self.schedule.add(agent)

    def is_there_a_car(self, cell):
        if cell.type == 'car':
            return True
        return False

    # Adds a agent car to grid and schedule
    def add_car(self):
        # Adds car agent
        destination = random.choice(self.parking_coords)
        # Defines its destination
        agent = Car(f"c{self.unique_id}", self, destination)
        # While they are the same
        allowed = False
        while not allowed:
            temp_allowed = []
            # Defines where it starts
            start = random.choice(self.parking_coords)
            print(start)
            if start != destination:
                # Can't appear if there is a car in next_cell
                astar = Astar(self, start, destination)
                path = astar.get_shortest_path()
                if path:
                    content = self.grid.get_cell_list_contents(path[0])
                    for a in content:
                        if self.is_there_a_car(a):
                            temp_allowed.append(True)

                # Can't appear if there is a car in the parking
                content = self.grid.get_cell_list_contents(start)
                for a in content:
                    if self.is_there_a_car(a):
                        temp_allowed.append(True)
            if len(temp_allowed) == 0:
                allowed = True

        # Adds agent to grid
        self.grid.place_agent(agent, start)
        self.schedule.add(agent)
        self.unique_id += 1

    def step(self):
        # Adds car every 10 seconds
        if self.num_steps % 10 == 0:
            self.add_car()
        # Carro sale (Test)
        elif self.num_steps == 3:
            agent = Car(f"c{1000}", self, (18, 20))
            self.grid.place_agent(agent, (18, 14))
            self.schedule.add(agent)
        '''Advance the model by one step.'''
        self.num_steps += 1
        self.schedule.step()
