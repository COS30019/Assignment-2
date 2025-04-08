import sys

class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self.origin = None
        self.destinations = []

    def parse_file(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                if line.startswith("Nodes"):
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
                    self.nodes[node_id] = (x, y)
                elif mode == "edges":
                    edge, cost = line.split(":")
                    start, end = map(int, edge.strip()[1:-1].split(','))
                    self.edges[(start, end)] = int(cost)
                elif mode == "origin":
                    self.origin = int(line)
                elif mode == "destinations":
                    self.destinations = [int(destination.strip) for destination in line.split(';')]
        
    def find_adjacent(self, node_id):
        adjacent = []
        for (start, end), cost in self.edges.items():
            if start == node_id:
                adjacent.append((end, cost))
        adjacent.sort()
        return adjacent
    
def dfs(graph):

def main():
        
# ------------------------
# A* Search
# ------------------------
def astar(nodes, edges, origin, goals):
    frontier = [(h(nodes, origin, goals), origin, [origin], 0)]
    explored = set()
    created = 1
    while frontier:
        f, node, path, g = heapq.heappop(frontier)
        if node in goals:
            return node, created, path
        explored.add(node)
        for neighbor, cost in edges.get(node, []):
            if neighbor not in explored:
                g_new = g + cost
                f_new = g_new + h(nodes, neighbor, goals)
                heapq.heappush(frontier, (f_new, neighbor, path + [neighbor], g_new))
                created += 1
    return None, created, []



