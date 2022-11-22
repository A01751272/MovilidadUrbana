from mesa import Agent
from astar import Astar


# Car agent
class Car(Agent):
    def __init__(self, unique_id, model, destination):
        super().__init__(unique_id, model)
        self.type = 'car'
        self.destination = destination
        self.priority = 3
        self.cant_move = True

    def can_move(self, next_cell):
        content = self.model.grid.get_cell_list_contents(self.pos)
        for agent in content:
            if agent.type == 'light':
                if not agent.state:
                    self.cant_move = True
                    return
        # Reserve the next cell
        self.model.reserved_cells[self.unique_id] = next_cell
        # Add the priorities to a specific cell
        if next_cell not in self.model.reserved_cells:
            self.model.reserved_cells[next_cell] = [self.priority]
        else:
            self.model.reserved_cells[next_cell].append(self.priority)

    def step(self):
        # If it has appeared, wait 1 step
        if not self.cant_move:
            # Get shortest path to destination
            astar = Astar(self.model, self.pos, self.destination)
            path = astar.get_shortest_path()

            # Delete agent if it has reached his destination
            if not path:
                self.model.grid.remove_agent(self)
                self.model.schedule.remove(self)
            else:
                self.can_move(path[0])

    def is_there_a_car(self, next_cell):
        content = self.model.grid.get_cell_list_contents(next_cell)
        for agent in content:
            if agent.type == 'car':
                return True
        return False

    def step2(self):
        next_move = self.pos
        if not self.cant_move:
            next_cell = self.model.reserved_cells[self.unique_id]
            priorities = self.model.reserved_cells[next_cell]
            if len(priorities) <= 1:
                if not self.is_there_a_car(next_cell):
                    next_move = next_cell
                    self.priority = 1
            else:
                if self.priority >= max(priorities):
                    if not self.is_there_a_car(next_cell):
                        next_move = next_cell
                        self.priority = 1
                        self.model.reserved_cells[next_cell].append(
                            max(priorities) + 1)
        self.model.grid.move_agent(self, next_move)

    def step3(self):
        self.cant_move = False
        self.model.reserved_cells = {}

    def step4(self):
        pass


# Traffic light agent
class Traffic_Light(Agent):
    def __init__(self, unique_id, model, direction):
        super().__init__(unique_id, model)
        self.type = 'light'
        self.direction = direction
        # If it is green or red
        self.state = False

    def step(self):
        pass

    def step2(self):
        pass

    def step3(self):
        pass

    def step4(self):
        pass

# Destination agent
class Destination(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = 'parking'

    def step(self):
        pass

    def step2(self):
        pass

    def step3(self):
        pass

    def step4(self):
        pass

# Building agent
class Building(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = 'building'

    def step(self):
        pass

    def step2(self):
        pass

    def step3(self):
        pass

    def step4(self):
        pass

# Road agent
class Road(Agent):
    def __init__(self, unique_id, model, direction):
        super().__init__(unique_id, model)
        self.type = 'road'
        self.direction = direction

    def step(self):
        pass

    def step2(self):
        pass

    def step3(self):
        pass

    def step4(self):
        pass