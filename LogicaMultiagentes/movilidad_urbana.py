from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation


class CarAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.next_state = None
        self.color = 0

    def step(self):
        if self.color == 0:
            self.next_state = 1
        else:
            self.next_state = 0

    def advance(self):
        self.color = self.next_state


class TrafficLightAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        ...

    def advance(self):
        ...


class MovilidadUrbana(Model):
    def __init__(self, width, height):
        self.grid = MultiGrid(width, height, False)
        self.schedule = SimultaneousActivation(self)
        self.running = True  # Para la visualizacion usando navegador

        car = CarAgent(0, self)
        self.schedule.add(car)
        self.grid.place_agent(car, (width//2, height//2))

    def step(self):
        self.schedule.step()
