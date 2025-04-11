import sys
import math

def populate_graph(filename):
    nodes = {}
    edges = {}
    origin = None
    destinations = []
    mode = None

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            if line.startswith("Nodes:"):
                mode = "nodes"
                continue
            elif line.startswith("Edges:"):
                mode= "edges"
                continue
            elif line.startswith("Origin:"):
                mode = "origin"
                continue
            elif line.startswith("Destinations:"):
                mode = "destinations"
                continue

            if mode == "nodes":
                node_id, coords = line.split(":")
                node_id = int(node_id)
                x, y = map(int, coords.strip()[1:-1].split(','))
                nodes[node_id] = (x, y)
            elif mode == "edges":
                edge, cost = line.split(":")
                start, end = map(int, edge.strip()[1:-1].split(','))
                edges[(start, end)] = float(cost)
            elif mode == "origin":
                origin = int(line)
            elif mode == "destinations":
                destinations = [int(destination.strip()) for destination in line.split(';')]
                
    return nodes, edges, origin, destinations
        
def find_adjacent(node_id, edges):
    adjacent = []
    for (start, end), cost in edges.items():
        if start == node_id:
            adjacent.append((end, cost))
    adjacent.sort()
    
    return adjacent

def euclidean(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def compute_heuristic(nodes, current, goals):
    return min(euclidean(nodes[current], nodes[goal]) for goal in goals)
        
