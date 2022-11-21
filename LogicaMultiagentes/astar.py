from queue import PriorityQueue
from model import *


def get_light_direction(model, light, direction):
    right = model.grid.get_cell_list_contents((light[0]+1, light[1]))
    left = model.grid.get_cell_list_contents((light[0]-1, light[1]))
    up = model.grid.get_cell_list_contents((light[0], light[1]+1))
    down = model.grid.get_cell_list_contents((light[0], light[1]-1))

    if direction == "LightVer":
        if right[-1].direction == "Intersection" and (left[-1].direction == "Right" or left[-1].direction == "Left"):
        direction = [(light[0]+1, light[1]),
                     (light[0]-1, light[1])]
    elif direction == "LightHor":
        direction = [(light[0], light[1]+1),
                     (light[0], light[1]-1)]
    return direction


def get_direction(model, current):
    direction = None
    cell = model.grid.get_cell_list_contents(current)
    for agent in cell:
        if agent.color == 'road':
            direction = agent.direction
        elif agent.color == 'light':
            direction = agent.direction
    if direction == "Right":
        direction = [(current[0]+1, current[1])]
    elif direction == "Left":
        direction = [(current[0]-1, current[1])]
    elif direction == "Up":
        direction = [(current[0], current[1]+1)]
    elif direction == "Down":
        direction = [(current[0]+1, current[1]-1)]
    elif direction == "Intersection":
        direction = None
    elif direction == "LightVer" or direction == "LightHor":
        direction = get_light_direction(model, current, direction)
    return direction


def get_neighbors(model, current):
    available_neighbors = []
    direction = get_direction(model, current)
    neighbors = model.grid.get_neighborhood(
        current,
        moore=False,
        include_center=False)
    for neighbor in neighbors:
        content = model.grid.get_cell_list_contents(neighbor)
        for agent in content:
            if agent.color in ['light', 'road']:
                if not direction:
                    available_neighbors.append(neighbor)
                elif neighbor in direction:
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
        print(current, neighbors)
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
