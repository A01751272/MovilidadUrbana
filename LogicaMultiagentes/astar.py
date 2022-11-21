from mesa.model import Model
# from grid_manager import NodeTypes
# from grid_manager import Node, h
from queue import PriorityQueue
from model import *


def get_neighbors(model, current):
    available_neighbors = []
    neighbors = model.grid.get_neighborhood(
        current,
        moore=False,
        include_center=False)
    for neighbor in neighbors:
        content = model.grid.get_cell_list_contents(neighbor)
        for agent in content:
            if agent.color in ['light', 'road']:
                available_neighbors.append(neighbor)
    return available_neighbors


def get_nodes_in_path(came_from, current):
    path = []
    while current in came_from:
        path.append((current[0], current[1]))
        current = came_from[current]
    path.reverse()
    print(path)
    return path


def manhattan_distance(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])


def get_shortest_path(model, start, end):
    g_score, f_score = {}, {}
    visited = []
    for (a, x, y) in model.grid.coord_iter():
        g_score[(x, y)] = float("inf")
        f_score[(x, y)] = float("inf")

    # Initialize counter, queue and set
    count = 0
    open_set = PriorityQueue()  # type: ignore
    open_set.put((0, count, start))
    came_from = {}  # type: ignore
    # Declare start node's scores
    g_score[start] = 0
    f_score[start] = manhattan_distance(start, end)  # type: ignore
    # Returns nodes in priority queue
    open_set_hash = {start}
    # Run until the open set is empty
    while not open_set.empty():
        # Current node will be the start node
        current = open_set.get()[2]
        # Remove current node from the open set hash
        open_set_hash.remove(current)
        # Check if current node is already the destination
        if current == end:
            return get_nodes_in_path(came_from, current)
        # Check the neighbors of the current node and add a temporary g score
        neighbors = get_neighbors(model, current)
        for neighbor in neighbors:
            # Check each neighbor's g score and look for the smallest one
            temp_g = g_score[current] + 1
            if temp_g < g_score[neighbor]:
                # Tell program that the current path comes from the current node
                came_from[neighbor] = current
                # Set the neighbor's g score the new g score
                g_score[neighbor] = temp_g
                f_score[neighbor] = temp_g + manhattan_distance(neighbor, end)
                # If neighbor has not been visited, change it's state and add it to the priority queue
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    visited.append(neighbor)
                if current != start:
                    ...
                    # current.state = NodeTypes.CLOSED
    return []
