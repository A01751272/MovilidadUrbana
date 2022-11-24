from mesa import Agent
from astar import Astar


# Car agent
class Car(Agent):
    def __init__(self, unique_id, model, destination):
        """Initialize car agent."""
        super().__init__(unique_id, model)
        self.type = 'car'
        self.destination = destination
        self.priority = 3
        self.cant_move = True

    def __can_move(self, next_cell):
        """Check whether agent can move."""
        content = self.model.grid.get_cell_list_contents(self.pos)
        # If it is in traffic light, check state
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

    def __give_priority(self):
        """Asigns priority to car based on position."""
        x, y = self.pos
        priority = 1
        content = self.model.grid.get_cell_list_contents(self.pos)
        # If car is in parking
        for agent in content:
            if agent.type == 'parking':
                priority = 3
                break
        else:
            # If car is on main road
            if (x < 2 or x > self.model.width - 3) or \
               (y < 2 or x > self.model.height - 3):
                priority = 2
            else:
                priority = 1
        self.priority = priority

    def __get_out_of_path(self, path):
        neighbors = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center=False)
        for neighbor in neighbors:
            content = self.model.grid.get_cell_list_contents(neighbor)
            for a in content:
                if a.type == 'car':
                    break
            else:
                if neighbor != path:
                    self.model.grid.move_agent(self, neighbor)
                    return True
        return False

    def step(self):
        """First step in schedule."""
        # If it has just appeared, wait 1 step
        if not self.cant_move:
            astar = Astar(self.model, self.pos, self.destination)
            path = astar.get_path()
            # Delete agent if it has reached his destination
            if not path:
                self.model.grid.remove_agent(self)
                self.model.schedule.remove(self)
            else:
                self.__give_priority()
                self.__can_move(path[0])

    def step2(self):
        """Second step in schedule."""
        next_move = self.pos
        # If car can't move
        if not self.cant_move:
            next_cell = self.model.reserved_cells[self.unique_id]
            priorities = self.model.reserved_cells[next_cell]
            is_there_a_car = self.__is_there_a_car(next_cell)
            # If there is only one car reserving that cell
            if len(priorities) <= 1:
                # If there isn't a car in next cell
                if not is_there_a_car:
                    next_move = next_cell
                else:
                    self.model.couldnt_move[self.pos] = next_cell
                    self.model.couldnt_move_ids[self.unique_id] = self.pos
            else:
                # If you have the highest priority
                if self.priority >= max(priorities):
                    # If there isn't a car in next cell
                    if not is_there_a_car:
                        next_move = next_cell
                        self.model.reserved_cells[next_cell].append(
                            max(priorities) + 1)
                    else:
                        self.model.couldnt_move[self.pos] = next_cell
                        self.model.couldnt_move_ids[self.unique_id] = self.pos
                else:
                    pass
                    # self.model.couldnt_move[self.pos] = next_cell
                    # self.model.couldnt_move_ids[self.unique_id] = self.pos

        self.model.grid.move_agent(self, next_move)

    def step3(self):
        if self.unique_id in self.model.couldnt_move_ids:
            astar = Astar(self.model, self.pos, self.destination)
            path = astar.get_path()
            if path:
                if path[0] in self.model.couldnt_move:
                    if self.model.couldnt_move[path[0]] == self.pos:
                        if self.__get_out_of_path(path[0]):
                            del self.model.couldnt_move[path[0]]
                else:
                    print(self.unique_id, "Ando formado")
        """Third step in schedule."""
        self.cant_move = False


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
        # TODO (Decide if it is green or red)
        if self.direction == 'light_vertical':
            self.state = True
        else:
            self.state = False

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
        while True:
            if self.model.grid.out_of_bounds(cell):
                return
            content = self.model.grid.get_cell_list_contents(cell)
            cars = 0
            for a in content:
                if cell != self.pos:
                    if a.type in ['building', 'parking', 'light']:
                        return
                    elif a.type == 'car':
                        cars += 1
                else:
                    if a.type in ['building', 'parking']:
                        return
                    elif a.type == 'car':
                        cars += 1
            self.num_cars += cars
            cell = (cell[0] + next[0], cell[1] + next[1])

    def __get_cars_in_line(self, direction):
        if direction == 'right':
            self.__count_cars((1, 0))
        elif direction == 'left':
            self.__count_cars((-1, 0))
        elif direction == 'up':
            self.__count_cars((0, 1))
        elif direction == 'down':
            self.__count_cars((0, -1))

    def step(self):
        # TODO (Change traffic light state)
        if self.model.num_steps % 5 == 0:
            self.state = not self.state

    def step2(self):
        direction = self.__get_light_direction()
        self.__get_cars_in_line(direction)

    def step3(self):
        # print("Position: ", self.pos, 
        # " My pair is: ", self.pair, " My quadrant is: ", self.quadrant)
        self.num_cars = 0


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
