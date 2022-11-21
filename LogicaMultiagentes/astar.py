from queue import PriorityQueue
from model import *


class Astar():
    def create_map(self):
        for (a, x, y) in self.model.grid.coord_iter():
            self.g_score[(x, y)] = float("inf")
            self.f_score[(x, y)] = float("inf")

    def manhattan_distance(self, start, end):
        return abs(start[0] - end[0]) + abs(start[1] - end[1])

    def __init__(self, model, start, end):
        # Create g and f for algorithm
        self.g_score = {}
        self.f_score = {}
        # Import model and create map
        self.model = model
        self.create_map()

        # Variables for algorithm
        self.count = 0
        self.start = start
        self.end = end
        self.open_set = PriorityQueue()
        self.open_set.put((0, self.count, self.start))
        self.came_from = {}
        # Declare start node's scores
        self.g_score[self.start] = 0
        self.f_score[self.start] = self.manhattan_distance(
            self.start, self.end)
        # Returns nodes in priority queue
        self.open_set_hash = {self.start}

    def get_light_direction(self, light, direction):
        dir = []

        if direction == "light_vertical":
            right = self.model.grid.get_cell_list_contents((
                light[0]+1, light[1]))
            left = self.model.grid.get_cell_list_contents((
                light[0]-1, light[1]))
            if right[0].direction == "intersection":
                dir = [(light[0]+1, light[1])]
            elif left[0].direction == "intersection":
                dir = [(light[0]-1, light[1])]
        elif direction == "light_horizontal":
            up = self.model.grid.get_cell_list_contents((
                light[0], light[1]+1))
            down = self.model.grid.get_cell_list_contents((
                light[0], light[1]-1))
            if up[0].direction == "intersection":
                dir = [(light[0], light[1]+1)]
            elif down[0].direction == "intersection":
                dir = [(light[0], light[1]-1)]
        return dir

    def get_direction(self, current):
        direction = None
        cell = self.model.grid.get_cell_list_contents(current)
        for agent in cell:
            if agent.type == 'road':
                direction = agent.direction
            elif agent.type == 'light':
                direction = agent.direction
        if direction == "right":
            direction = [(current[0]+1, current[1])]
        elif direction == "left":
            direction = [(current[0]-1, current[1])]
        elif direction == "up":
            direction = [(current[0], current[1]+1)]
        elif direction == "down":
            direction = [(current[0], current[1]-1)]
        elif direction == "intersection":
            direction = None
        elif direction == "light_vertical" or \
                direction == "light_horizontal":
            direction = self.get_light_direction(current, direction)
        return direction

    def get_neighbors(self, current):
        available_neighbors = []
        direction = self.get_direction(current)
        neighbors = self.model.grid.get_neighborhood(
            current,
            moore=False,
            include_center=False)
        for neighbor in neighbors:
            content = self.model.grid.get_cell_list_contents(neighbor)
            for agent in content:
                if agent.type == 'parking' and neighbor == self.end:
                    return [neighbor]
                if agent.type in ['light', 'road']:
                    if not direction:
                        available_neighbors.append(neighbor)
                    elif neighbor in direction:
                        available_neighbors.append(neighbor)
        return available_neighbors

    def get_nodes_in_path(self, current):
        path = []
        while current in self.came_from:
            path.append((current[0], current[1]))
            current = self.came_from[current]
        path.reverse()
        return path

    def get_shortest_path(self):
        while not self.open_set.empty():
            # Current node will be the start node
            current = self.open_set.get()[2]
            # Remove current node from the open set hash
            self.open_set_hash.remove(current)
            # Check if current node is already the destination
            if current == self.end:
                return self.get_nodes_in_path(current)
            # Check the neighbors of the current node and
            # add a temporary g score
            neighbors = self.get_neighbors(current)
            for neighbor in neighbors:
                # Check each neighbor's g score and look for the smallest one
                temp_g = self.g_score[current] + 1
                if temp_g < self.g_score[neighbor]:
                    # Tell program that the current path comes
                    # from the current node
                    self.came_from[neighbor] = current
                    # Set the neighbor's g score the new g score
                    self.g_score[neighbor] = temp_g
                    self.f_score[neighbor] = temp_g + self.manhattan_distance(
                        neighbor, self.end)
                    # If neighbor has not been visited, change it's state and
                    # add it to the priority queue
                    if neighbor not in self.open_set_hash:
                        self.count += 1
                        self.open_set.put((self.f_score[neighbor],
                                           self.count, neighbor))
                        self.open_set_hash.add(neighbor)
        return []
