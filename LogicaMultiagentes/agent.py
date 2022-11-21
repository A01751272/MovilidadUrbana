from mesa import Agent


class Car(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.color = 'car'

    def step(self):
        pass


class Traffic_Light(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.state = False
        self.color = 'light'

    def step(self):
        pass


class Destination(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.color = 'park'

    def step(self):
        pass


class Building(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.color = 'building'

    def step(self):
        pass


class Road(Agent):
    def __init__(self, unique_id, model, direction):
        super().__init__(unique_id, model)
        self.direction = direction
        self.color = 'road'

    def step(self):
        pass
