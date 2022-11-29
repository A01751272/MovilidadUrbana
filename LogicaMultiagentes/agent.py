from mesa import Agent
from astar import Astar
from math import floor


# Car agent
class Car(Agent):
    def __init__(self, unique_id, model, destination):
        """Initialize car agent."""
        super().__init__(unique_id, model)
        self.type = 'car'
        self.destination = destination
        self.priority = 3
        self.prev = None
        self.cant_move = True
        self.has_changed_lane = False
        self.reached_destination = False

    def __can_move(self, next_cell):
        """Check whether agent can move."""
        # Check if agent is in a red traffic light
        content = self.model.grid.get_cell_list_contents(self.pos)
        for agent in content:
            if agent.type == 'light':
                if not agent.state:
                    self.cant_move = True
                    return

        # Reserve the next cell
        self.model.reserved_cells[self.unique_id] = next_cell
        # Add the priorities to the next cell
        if next_cell not in self.model.reserved_cells:
            self.model.reserved_cells[next_cell] = [self.priority]
        else:
            self.model.reserved_cells[next_cell].append(self.priority)

    def __is_there_a_car(self, next_cell):
        """Checks whether there is a car in next cell."""
        content = self.model.grid.get_cell_list_contents(next_cell)
        for agent in content:
            if agent.type == 'car':
                return True
        return False

    def __is_there_a_obstacle(self, next_cell):
        """Checks whether there is an obstacle in next cell."""
        content = self.model.grid.get_cell_list_contents(next_cell)
        for agent in content:
            if agent.type in ['car', 'building', 'parking']:
                return True
        return False

    def __give_priority(self):
        """Asigns priority to car based on position."""
        x, y = self.pos
        priority = 1
        content = self.model.grid.get_cell_list_contents(self.pos)
        # Parking = 3
        for agent in content:
            if agent.type == 'parking':
                priority = 3
                break
        else:
            # Main road = 2
            if (x < 2 or x > self.model.width - 3) or \
               (y < 2 or x > self.model.height - 3):
                priority = 2
            # Central road = 1
            else:
                priority = 1
        self.priority = priority

    def __get_out_of_path(self, path):
        """If both cars are stuck by each other."""
        neighbors = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center=False)
        for neighbor in neighbors:
            content = self.model.grid.get_cell_list_contents(neighbor)
            for a in content:
                if a.type in ['car', 'building', 'parking']:
                    break
            else:
                if neighbor != path:
                    return neighbor
        return False

    def __can_change_to(self):
        """Check what direction a car can change to."""
        direction = None
        cell = self.model.grid.get_cell_list_contents(self.pos)

        # Check type of cell
        for agent in cell:
            if agent.type == 'road':
                direction = agent.direction
                break

        # Check which way it can't move
        if direction == "intersection":
            if self.prev == "right":
                direction = "right"
            elif self.prev == "left":
                direction = "left"
            elif self.prev == "up":
                direction = "up"
            elif self.prev == "down":
                direction = "down"

        # Get next directions from current cell
        if direction == "right":
            # Can´t move left
            direction = [(self.pos[0], self.pos[1]+1),
                         (self.pos[0], self.pos[1]-1),
                         (self.pos[0] + 1, self.pos[1])]
        elif direction == "left":
            # Can't move right
            direction = [(self.pos[0], self.pos[1]+1),
                         (self.pos[0], self.pos[1]-1),
                         (self.pos[0] - 1, self.pos[1])]
        elif direction == "up":
            # Can't move down
            direction = [(self.pos[0]+1, self.pos[1]),
                         (self.pos[0]-1, self.pos[1]),
                         (self.pos[0], self.pos[1] + 1)]
        elif direction == "down":
            # Can't move up
            direction = [(self.pos[0]+1, self.pos[1]),
                         (self.pos[0]-1, self.pos[1]),
                         (self.pos[0], self.pos[1] - 1)]
        else:
            direction = None
        return direction

    def __calculate_prev(self):
        cell = self.model.grid.get_cell_list_contents(self.pos)
        direction = None
        for agent in cell:
            if agent.type in ['road', 'light']:
                direction = agent.direction
                break
        if direction:
            if direction in ['intersection', 'light_vertical',
                             'light_vertical']:
                return False
            self.prev = direction
            return True
        return False

    def __change_lanes(self):
        """Car changes lanes if it is available."""
        cells_move = self.__can_change_to()
        if cells_move:
            for neighbor in cells_move:
                if not self.model.grid.out_of_bounds(neighbor):
                    if not self.__is_there_a_obstacle(neighbor):
                        self.has_changed_lane = True  # TODO
                        self.__calculate_prev()
                        self.model.grid.move_agent(self, neighbor)
                        return True
        # Car couldn't change lanes
        return False

    def step(self):
        print(self.unique_id, self.pos, self.prev)
        """First step in schedule."""
        # If car can move
        if not self.cant_move:
            # TODO
            astar = Astar(self.model, self.pos, self.destination)
            path = astar.get_path()
            # Delete agent if it has reached his destination
            if not path:
                # Wait 1 second before disappearing
                # Checks whether car has reached destination
                if not self.reached_destination:
                    self.reached_destination = True
                # Disappear agent
                else:
                    self.model.grid.remove_agent(self)
                    self.model.schedule.remove(self)
            # If car can move
            else:
                self.__give_priority()
                self.__can_move(path[0])
        # If car can't move
        else:
            pass

    def step2(self):
        """Second step in schedule."""
        # If car can move
        if not self.cant_move and not self.reached_destination:
            next_move = self.pos

            next_cell = self.model.reserved_cells[self.unique_id]
            priorities = self.model.reserved_cells[next_cell]
            is_there_a_car = self.__is_there_a_car(next_cell)

            # If there is only one car reserving that cell
            if len(priorities) <= 1:
                # If there isn't a car in next cell
                if not is_there_a_car:
                    next_move = next_cell
                    self.has_changed_lane = False
                else:
                    self.model.couldnt_move[self.pos] = next_cell
                    self.model.couldnt_move_ids[self.unique_id] = self.pos
            # If there are multiple cars in next cell
            else:
                # If you have the highest priority
                if self.priority >= max(priorities):
                    if not is_there_a_car:
                        next_move = next_cell
                        self.has_changed_lane = False
                        self.model.reserved_cells[next_cell].append(
                            max(priorities) + 1)
                    else:
                        self.model.couldnt_move[self.pos] = next_cell
                        self.model.couldnt_move_ids[self.unique_id] = self.pos
                else:
                    # Someone with higher priority has taken next cell
                    pass
            self.__calculate_prev()
            self.model.grid.move_agent(self, next_move)
        # If car can't move
        else:
            pass

    def step3(self):
        """Third step in schedule."""
        # If car couldn't move before
        if not self.cant_move and not self.reached_destination:
            if self.unique_id in self.model.couldnt_move_ids:
                # TODO
                astar = Astar(self.model, self.pos, self.destination)
                path = astar.get_path()
                # Someone who couldn't move is in your next cell
                if path[0] in self.model.couldnt_move:
                    # Next cell car is looking at this car position
                    if self.model.couldnt_move[path[0]] == self.pos:
                        can_exit_path = self.__get_out_of_path(path[0])
                        if can_exit_path:
                            del self.model.couldnt_move[self.pos]
                            self.__calculate_prev()
                            self.model.grid.move_agent(self, can_exit_path)
                    # Next cell car is not looking at this car position
                    else:
                        if not self.has_changed_lane:
                            self.__change_lanes()
                        else:
                            pass
                # No one who couldn't move is in your next cell
                else:
                    is_there_a_car = self.__is_there_a_car(path[0])
                    if not is_there_a_car:
                        self.__calculate_prev()
                        self.model.grid.move_agent(self, path[0])
                    elif not self.has_changed_lane:
                        self.__change_lanes()
                    else:
                        pass
            else:
                # If car moved last step
                pass
        # If car can't move
        else:
            pass

    def step4(self):
        """Fourth step in schedule."""
        self.cant_move = False
        self.model.reserved_cells = {}
        self.model.couldnt_move = {}
        self.model.couldnt_move_ids = {}


# Traffic light agent
class Traffic_Light(Agent):
    def __init__(self, unique_id, model, direction):
        """Initialize traffic light agent."""
        super().__init__(unique_id, model)
        self.type = 'light'
        self.direction = direction
        self.num_cars = 0
        self.pair = None
        self.quadrant = None
        self.seconds = 0
        self.green = False
        # TODO (Decide if it is green or red)
        if self.direction == 'light_vertical':
            self.state = True
        else:
            self.state = False
        # self.state = False

    def __get_light_direction(self):
        """Get direction from traffic light."""
        dir = None
        # Checks type of traffic light
        if self.direction == "light_vertical":
            right = self.model.grid.get_cell_list_contents((
                self.pos[0]+1, self.pos[1]))
            left = self.model.grid.get_cell_list_contents((
                self.pos[0]-1, self.pos[1]))
            # Get next directions from current cell
            if right[0].direction == "intersection":
                dir = 'right'
            elif left[0].direction == "intersection":
                dir = 'left'
        elif self.direction == "light_horizontal":
            up = self.model.grid.get_cell_list_contents((
                self.pos[0], self.pos[1]+1))
            down = self.model.grid.get_cell_list_contents((
                self.pos[0], self.pos[1]-1))
            # Get next directions from current cell
            if up[0].direction == "intersection":
                dir = 'up'
            elif down[0].direction == "intersection":
                dir = 'down'
        return dir

    def __count_cars(self, next):
        cell = self.pos
        cont = 0
        while cont < 6:
            if self.model.grid.out_of_bounds(cell):
                return
            content = self.model.grid.get_cell_list_contents(cell)
            for a in content:
                if cell != self.pos:
                    if a.type in ['building', 'parking', 'light']:
                        return
                    elif a.type == 'car':
                        self.num_cars += 1
                else:
                    if a.type in ['building', 'parking']:
                        return
                    elif a.type == 'car':
                        self.num_cars += 1
            cell = (cell[0] + next[0], cell[1] + next[1])
            cont += 1

    def __get_cars_in_line(self, direction):
        if direction == 'right':
            self.__count_cars((-1, 0))
        elif direction == 'left':
            self.__count_cars((1, 0))
        elif direction == 'up':
            self.__count_cars((0, -1))
        elif direction == 'down':
            self.__count_cars((0, 1))

    def __add_pairs(self):
        if self.quadrant not in self.model.cuadrant_pairs:
            self.model.cuadrant_pairs[self.quadrant] = {}
        if self.pair not in self.model.cuadrant_pairs[self.quadrant]:
            self.model.cuadrant_pairs[self.quadrant][self.pair] = \
                    self.num_cars
        else:
            self.model.cuadrant_pairs[self.quadrant][self.pair] += \
                    self.num_cars

    def restart_variables(self):
        self.seconds = 0
        self.green = False
        self.model.change_value = []
        self.model.cuadrant_considered = []
        self.model.assign_seconds = {}
        self.state = False
        self.num_cars = 0

    def decide_color(self):
        quadrant = self.model.cuadrant_pairs[self.quadrant]
        if self.quadrant not in self.model.cuadrant_considered:
            max_value = float('-inf')
            max_key = 0
            total = 0
            for key, value in quadrant.items():
                total += value
                if value > max_value:
                    max_value = value
                    max_key = key
            if total:
                seconds = floor((max_value/total)*10)
            else:
                seconds = 5
            self.model.assign_seconds[max_key] = seconds
            self.model.cuadrant_considered.append(self.quadrant)
        if self.pair in self.model.assign_seconds:
            self.seconds = self.model.assign_seconds[self.pair]
            self.green = True
            self.state = True
        # print(self.unique_id, self.quadrant, self.pair, self.pos,
        # self.num_cars, self.seconds, self.state)

    def step(self):
        # print(self.unique_id, self.pos, self.num_cars,
        #      self.state, self.seconds)
        if self.model.num_steps % 10 == 0:
            ...
        else:
            if self.green:
                if self.seconds <= 0:
                    self.model.change_value.append(self.quadrant)
                    # self.state = not self.state
                else:
                    self.seconds -= 1

    def step2(self):
        # print(self.unique_id, self.num_cars)
        if self.model.num_steps % 10 == 0:
            self.model.cuadrant_pairs = {}
        else:
            if self.quadrant in self.model.change_value:
                self.state = not self.state
                self.green = False

    def step3(self):
        # self.model.change_value = []
        if self.model.num_steps % 10 == 0:
            self.restart_variables()
            direction = self.__get_light_direction()
            self.__get_cars_in_line(direction)
            self.__add_pairs()
        else:
            self.model.change_value = []

    def step4(self):
        if self.model.num_steps % 10 == 0:
            self.decide_color()


# Destination agent (Doesn't have a scheduler)
class Destination(Agent):
    def __init__(self, unique_id, model):
        """Initialize destination agent."""
        super().__init__(unique_id, model)
        self.type = 'parking'


# Road agent (Doesn't have a scheduler)
class Road(Agent):
    def __init__(self, unique_id, model, direction):
        """Initialize road agent."""
        super().__init__(unique_id, model)
        self.type = 'road'
        self.direction = direction


# Building agent (Doesn't have a scheduler)
class Building(Agent):
    def __init__(self, unique_id, model):
        """Initialize building agent."""
        super().__init__(unique_id, model)
        self.type = 'building'
