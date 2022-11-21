from mesa import Agent
from astar import Astar


# Car agent
class Car(Agent):
    def __init__(self, unique_id, model, destination):
        super().__init__(unique_id, model)
        self.type = 'car'
        self.destination = destination

    def step(self):
        # Get shortest path to destination
        astar = Astar(self.model, self.pos, self.destination)
        path = astar.get_shortest_path()
        if path:
            # Move agent to next neighbor
            self.model.grid.move_agent(self, path[0])


# Traffic light agent
class Traffic_Light(Agent):
    def __init__(self, unique_id, model, direction):
        super().__init__(unique_id, model)
        self.type = 'light'
        self.direction = direction
        # If it is green or red
        self.state = True

    def step(self):
        pass


# Destination agent
class Destination(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = 'parking'

    def step(self):
        pass


# Building agent
class Building(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = 'building'

    def step(self):
        pass


# Road agent
class Road(Agent):
    def __init__(self, unique_id, model, direction):
        super().__init__(unique_id, model)
        self.type = 'road'
        self.direction = direction

    def step(self):
        pass
