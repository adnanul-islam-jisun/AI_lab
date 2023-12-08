import heapq
import math
import csv
from collections import defaultdict

COORDINATES_FILE = r"E:\University\Programming\Pyhon\Assigenment\Coordinates.csv"
DISTANCE_FILE = r"E:\University\Programming\Pyhon\Assigenment\distances.csv"

def euclidean_distance(coord1, coord2):
    return sum((x - y) ** 2 for x, y in zip(coord1, coord2)) ** 0.5

def get_neighbors(star, distances):
    neighbors = []
    for (source, dest), distance in distances.items():
        if source == star:
            neighbors.append((dest, distance))
        elif dest == star:
            neighbors.append((source, distance))
    return neighbors

def load_coordinates():
    coordinates = {}
    with open(COORDINATES_FILE, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for star_name, x, y, z in reader:
            coordinates[star_name] = (int(x), int(y), int(z))
    return coordinates

def load_distances():
    distances = {}
    with open(DISTANCE_FILE, "r") as file:
        reader = csv.reader(file)
        for source, destination, dist in reader:
            distances[(source, destination)] = int(dist)
    return distances

def dijkstra(start, end, distances):
    min_heap = [(0, start, [])]
    visited = set()

    while min_heap:
        cost, node, path = heapq.heappop(min_heap)

        if node in visited:
            continue

        path = path + [node]
        if node == end:
            return path, cost

        visited.add(node)

        for neighbor, o in get_neighbors(node, distances):
            if neighbor not in visited:
                heapq.heappush(min_heap, (cost + o, neighbor, path))

    return None, float('inf')

def a_star(start, end, distances, coordinates):
    def heuristic(node):
        return euclidean_distance(coordinates[node], coordinates[end])

    min_heap = [(0, start, [])]
    visited = set()

    while min_heap:
        cost, node, path = heapq.heappop(min_heap)

        if node in visited:
            continue

        path = path + [node]
        if node == end:
            return path, cost

        visited.add(node)

        for neighbor, N_Cost in get_neighbors(node, distances):
            if neighbor not in visited:
                heapq.heappush(min_heap, (cost + N_Cost + heuristic(neighbor), neighbor, path))

    return None, float('inf')

def print_result(name, path, cost, time,  reverse_path=True):
    print(f'{name} algorithm:')
    if reverse_path:
        path = path[::-1]
    print('Path:', ' -> '.join(path))
    print('Cost:', cost)
    print('Time:', time)
    print()

if __name__ == '__main__':
  
    start_star = 'Sun'
    end_star = 'HD 219134'

   
    coordinates = load_coordinates()
    distances = load_distances()

    import time
    start_time = time.time()
    dijkstra_path, dijkstra_cost = dijkstra(start_star, end_star, distances)
    dijkstra_time = time.time() - start_time

  
    start_time = time.time()
    a_star_path, a_star_cost = a_star(start_star, end_star, distances, coordinates)
    a_star_time = time.time() - start_time


    print_result('A*', a_star_path[::-1], a_star_cost, a_star_time)

    print_result('Dijkstra', dijkstra_path[::-1], dijkstra_cost, dijkstra_time)