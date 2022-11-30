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
        self.add_car_every = cars_every
        self.unique_id = 0
        # Parking
        self.parking_coords = []
        # Traffic light
        self.lights_coords = []
        # Car
        self.reserved_cells = {}
        self.cuadrant_pairs = {}
        self.cuadrant_considered = []
        self.assign_seconds = {}
        self.change_value = []
        self.couldnt_move = {}
        self.couldnt_move_ids = {}

        # Model variables
        map_dictionary_file = 'LogicaMultiagentes/map_dictionary.txt'
        map_file = 'LogicaMultiagentes/map.txt'
        map_dictionary = json.load(open(map_dictionary_file))

        # Reads the map
        with open(map_file) as map_file:
            lines = map_file.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)
            self.grid = MultiGrid(self.width, self.height, torus=False)
            self.schedule = StagedActivation(self, ['step', 'step2',
                                                    'step3', 'step4'])

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
                        # Add agent to scheduler after cars
                        self.lights_coords.append(agent)
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

        self.edge_positions = [(0, 0), (0, 1),
                               (0, self.height-1), (0, self.height-2),
                               (self.width - 1, self.height - 1),
                               (self.width - 1, self.height - 2),
                               (self.width - 1, 0), (self.width - 1, 1)]

        # Add n initial cars
        for _ in range(initial_cars):
            self.add_car()

        # Add trafic lights
        self.add_traffic_lights()

    def __car_in_cell(self, cell):
        """Checks if there is a car in a certain cell."""
        content = self.grid.get_cell_list_contents(cell)
        for a in content:
            if a.type == 'car':
                return True
        return False

    def __check_previous_cell(self, path, start):
        """Check if there is a car in previous cell"""
        previous_cell = None
        begin = path[0]
        next = path[1]

        # Determines previous cell
        if next[0] > begin[0]:
            previous_cell = (begin[0]-1, begin[1])
        elif next[0] < begin[0]:
            previous_cell = (begin[0]+1, begin[1])
        elif next[1] > begin[1]:
            previous_cell = (begin[0], begin[1]-1)
        elif next[1] < begin[1]:
            previous_cell = (begin[0], begin[1]+1)
        content = self.grid.get_cell_list_contents(previous_cell)

        # Can't appear if there is a car in previous cell
        for a in content:
            if a.type == 'car':
                if a.destination == start:
                    return False
        return True

    def __try_to_insert_car(self, is_random):
        """Try to insert car in any cell"""
        destination = random.choice(self.parking_coords)
        tries = 0
        allowed = False

        # While it isn't allowed to be placed in start parking
        while not allowed and tries < 10:
            if not is_random:
                start = random.choice(self.parking_coords)
            else:
                start = random.choice(self.edge_positions)
            # If start parking is different from destination
            if start != destination:
                astar = Astar(self, start, destination, 3)
                path = astar.get_path()
                # If there is a path
                if path:
                    if not is_random:
                        if not self.__car_in_cell(path[0]) and \
                                not self.__car_in_cell(start) and \
                                self.__check_previous_cell(path, start):
                            allowed = True
                    else:
                        if not self.__car_in_cell(path[0]) and \
                                not self.__car_in_cell(start):
                            allowed = True
            tries += 1
        if allowed:
            return [start, destination]
        return False

    def __add_car_random(self):
        """Adds car to random cell grid and schedule."""
        allowed = self.__try_to_insert_car(True)

        if allowed:
            astar = Astar(self, allowed[0], allowed[-1])
            path = astar.get_path()
            agent = Car(f"c{self.unique_id}", self, allowed[-1], path)

            # Adds agent to grid and schedule
            self.grid.place_agent(agent, allowed[0])
            self.schedule.add(agent)
            self.unique_id += 1

    # Adds a agent car to grid and schedule
    def add_car(self):
        """Adds car to grid and schedule."""
        allowed = self.__try_to_insert_car(False)

        # Adds agent to grid and schedule
        if allowed:
            astar = Astar(self, allowed[0], allowed[-1])
            path = astar.get_path()
            agent = Car(f"c{self.unique_id}", self, allowed[-1], path)

            # Adds agent to grid and schedule
            self.grid.place_agent(agent, allowed[0])
            self.schedule.add(agent)
            self.unique_id += 1
        else:
            self.__add_car_random()

    def add_traffic_lights(self):
        # Adds traffic lights to scheduler
        pair = 0
        quad = 0
        for count, a in enumerate(self.lights_coords):
            if count >= 18:
                if count == 18 or count == 19:
                    a.pair = pair + 1
                    a.quadrant = quad+1
                elif count == 20 or count == 22:
                    a.pair = pair+2
                    a.quadrant = quad
                elif count == 21 or count == 23:
                    a.pair = pair+3
                    a.quadrant = quad+1
            else:
                if count % 2 == 0:
                    pair += 1
                if count % 4 == 0:
                    quad += 1
                a.pair = pair
                a.quadrant = quad
            if a.quadrant not in self.cuadrant_pairs:
                self.cuadrant_pairs[a.quadrant] = {}
            if a.pair not in self.cuadrant_pairs[a.quadrant]:
                self.cuadrant_pairs[a.quadrant][a.pair] = 0
            self.schedule.add(a)
        return True

    def step(self):
        '''Advance the model by one step.'''
        # Adds car every n seconds
        if self.num_steps % self.add_car_every == 0:
            self.add_car()
        self.num_steps += 1
        self.schedule.step()
