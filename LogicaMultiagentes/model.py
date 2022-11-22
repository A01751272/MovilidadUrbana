from mesa import Model
from mesa.time import StagedActivation
from mesa.space import MultiGrid
import json
import random
from astar import Astar
from agent import Road, Traffic_Light, Building, Destination, Car


# City model
class CityModel(Model):
    # Initialize variables
    def __init__(self, initial_cars, cars_every):
        """Initialize model."""
        self.running = True
        self.num_steps = 0
        map_dictionary_file = 'LogicaMultiagentes/map_dictionary.txt'
        map_dictionary = json.load(open(map_dictionary_file))
        self.parking_coords = []
        map_file = 'LogicaMultiagentes/map.txt'
        self.reserved_cells = {}

        # Reads the map
        with open(map_file) as map_file:
            lines = map_file.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)
            self.grid = MultiGrid(self.width, self.height, torus=False)
            self.schedule = StagedActivation(self, ['step', 'step2', 'step3'])
            self.unique_id = 0

            # Adds agents to grid
            # For every row
            for r, row in enumerate(lines):
                # For every column
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
                        # Add agent to scheduler
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

        for _ in range(10):
            self.add_car()

        # TEST
        self.couldnt_move = {}
        self.couldnt_move_ids = {}

    def __car_in_cell(self, cell):
        """Checks if there is a car in a certain cell."""
        content = self.grid.get_cell_list_contents(cell)
        for a in content:
            # Can't appear if there is a car in the parking
            if a.type == 'car':
                return True
        return False

    def __check_previous_cell(self, path, start):
        """Check if there is a car in previous cell"""
        previous_cell = None
        begin = path[0]
        next = path[1]
        # Checks what direction does agent move
        if next[0] > begin[0]:
            previous_cell = (begin[0]-1, begin[1])
        elif next[0] < begin[0]:
            previous_cell = (begin[0]+1, begin[1])
        elif next[1] > begin[1]:
            previous_cell = (begin[0], begin[1]-1)
        elif next[1] < begin[1]:
            previous_cell = (begin[0], begin[1]+1)
        content = self.grid.get_cell_list_contents(previous_cell)
        for a in content:
            # Can't appear if there is a car in previous cell
            if a.type == 'car':
                if a.destination == start:
                    return False
        return True

    # Adds a agent car to grid and schedule
    def add_car(self):
        """Adds car to grid and schedule."""
        destination = random.choice(self.parking_coords)
        agent = Car(f"c{self.unique_id}", self, destination)
        allowed = False

        # While it isn't allowed to be placed in start parking
        while not allowed:
            start = random.choice(self.parking_coords)

            # If start parking is different from destination
            if start != destination:
                astar = Astar(self, start, destination)
                path = astar.get_shortest_path()
                # If there is a path
                if path:
                    if not self.__car_in_cell(path[0]) and \
                            not self.__car_in_cell(start) and \
                            self.__check_previous_cell(path, start):
                        allowed = True

        # Adds agent to grid and schedule
        self.grid.place_agent(agent, start)
        self.schedule.add(agent)
        self.unique_id += 1

    def step(self):
        '''Advance the model by one step.'''
        # Adds car every 10 seconds
        if self.num_steps % 1 == 0:
            self.add_car()
        self.num_steps += 1
        self.reserved_cells = {}
        self.couldnt_move = {}
        self.couldnt_move_ids = {}
        self.schedule.step()
