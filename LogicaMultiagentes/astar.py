from queue import PriorityQueue
from model import *


# A* search algorithm
class Astar():
    def __init__(self, model, start, end):
        """Initialize model."""
        self.g_score = {}
        self.f_score = {}
        self.model = model
        self.count = 0
        self.start = start
        self.end = end
        self.create_map()
        self.open_set = PriorityQueue()
        self.open_set.put((0, self.count, self.start))
        self.came_from = {}
        self.g_score[self.start] = 0
        self.f_score[self.start] = self.__manhattan_distance(
            self.start, self.end)
        self.open_set_hash = {self.start}

    def create_map(self):
        """Creates grid."""
        # Iterates through grid
        for (a, x, y) in self.model.grid.coord_iter():
            self.g_score[(x, y)] = float("inf")
            self.f_score[(x, y)] = float("inf")

    def __manhattan_distance(self, start, end):
        """Calculates the distance between two points."""
        return abs(start[0] - end[0]) + abs(start[1] - end[1])

    def __get_light_direction(self, light, direction):
        """Get direction from traffic light."""
        dir = []
        # Checks type of traffic light
        if direction == "light_vertical":
            right = self.model.grid.get_cell_list_contents((
                light[0]+1, light[1]))
            left = self.model.grid.get_cell_list_contents((
                light[0]-1, light[1]))
            # Get next directions from current cell
            if right[0].direction == "intersection":
                dir = [(light[0]+1, light[1])]
            elif left[0].direction == "intersection":
                dir = [(light[0]-1, light[1])]
        elif direction == "light_horizontal":
            up = self.model.grid.get_cell_list_contents((
                light[0], light[1]+1))
            down = self.model.grid.get_cell_list_contents((
                light[0], light[1]-1))
            # Get next directions from current cell
            if up[0].direction == "intersection":
                dir = [(light[0], light[1]+1)]
            elif down[0].direction == "intersection":
                dir = [(light[0], light[1]-1)]
        return dir

    def __get_direction(self, current):
        """Get direction from current cell."""
        direction = None
        cell = self.model.grid.get_cell_list_contents(current)
        # Check type of each cell
        for agent in cell:
            if agent.type == 'road':
                direction = agent.direction
            elif agent.type == 'light':
                direction = agent.direction
        # Get next directions from current cell
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
            direction = self.__get_light_direction(current, direction)
        return direction

    def __get_neighbors(self, current):
        """Get available neighbors to build path."""
        available_neighbors = []
        direction = self.__get_direction(current)
        neighbors = self.model.grid.get_neighborhood(
            current,
            moore=False,
            include_center=False)
        # Check each neighbor
        for neighbor in neighbors:
            content = self.model.grid.get_cell_list_contents(neighbor)
            # Check type of each cell
            for agent in content:
                if agent.type == 'parking' and neighbor == self.end:
                    return [neighbor]
                if agent.type in ['light', 'road']:
                    if not direction:
                        available_neighbors.append(neighbor)
                    elif neighbor in direction:
                        available_neighbors.append(neighbor)
        return available_neighbors

    def __get_nodes_in_path(self, current):
        """Get path from start to end."""
        path = []
        # Build path
        while current in self.came_from:
            path.append((current[0], current[1]))
            current = self.came_from[current]
        path.reverse()
        return path

    def get_shortest_path(self):
        while not self.open_set.empty():
            current = self.open_set.get()[2]
            self.open_set_hash.remove(current)
            # If current node is already the destination
            if current == self.end:
                return self.__get_nodes_in_path(current)
            neighbors = self.__get_neighbors(current)

            # Check each neighbor's g score and look for the smallest one
            for neighbor in neighbors:
                temp_g = self.g_score[current] + 1
                # If g score is smaller than current + 1
                if temp_g < self.g_score[neighbor]:
                    self.came_from[neighbor] = current
                    self.g_score[neighbor] = temp_g
                    self.f_score[neighbor] = temp_g + \
                        self.__manhattan_distance(
                        neighbor, self.end)
                    # If neighbor has not been visited, add to priority queue
                    if neighbor not in self.open_set_hash:
                        self.count += 1
                        self.open_set.put((self.f_score[neighbor],
                                           self.count, neighbor))
                        self.open_set_hash.add(neighbor)
        return []
