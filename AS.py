import heapq
import math
import sys

# ------------------------
# Input Parser
# ------------------------
def parse_input_file(filepath):
    nodes, edges = {}, {}
    origin, destinations = None, []
    section = None
    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            if line.startswith("Nodes:"):
                section = "nodes"
                continue
            elif line.startswith("Edges:"):
                section = "edges"
                continue
            elif line.startswith("Origin:"):
                section = "origin"
                continue
            elif line.startswith("Destinations:"):
                section = "destinations"
                continue

            if section == "nodes":
                node_id, coords = line.split(":")
                x, y = map(float, coords.strip().strip("()").split(","))
                nodes[int(node_id)] = (x, y)
            elif section == "edges":
                (n1, n2), cost = line.split(":"), float(line.split(":")[1])
                n1, n2 = map(int, line.split(":")[0].strip("() ").split(","))
                if n1 not in edges:
                    edges[n1] = []
                edges[n1].append((n2, cost))
            elif section == "origin":
                origin = int(line)
            elif section == "destinations":
                destinations = list(map(int, line.split(";")))

    return nodes, edges, origin, destinations

# ------------------------
# Heuristic
# ------------------------
def euclidean(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def h(nodes, current, goals):
    return min(euclidean(nodes[current], nodes[goal]) for goal in goals)

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

# ------------------------
# CUS2: Weighted Greedy Search
# ------------------------
def cus2(nodes, edges, origin, goals):
    frontier = [(0, origin, [origin])]
    explored = set()
    created = 1
    while frontier:
        f, node, path = heapq.heappop(frontier)
        if node in goals:
            return node, created, path
        explored.add(node)
        for neighbor, _ in edges.get(node, []):
            if neighbor not in explored:
                f_new = h(nodes, neighbor, goals) + len(path) * 0.5
                heapq.heappush(frontier, (f_new, neighbor, path + [neighbor]))
                created += 1
    return None, created, []

# ------------------------
# Main Runner
# ------------------------
def run(filename, method):
    nodes, edges, origin, goals = parse_input_file(filename)
    methods = {
        "AS": astar,
        "CUS2": cus2,
    }
    if method not in methods:
        return f"Invalid method: {method}"
    goal, created, path = methods[method](nodes, edges, origin, goals)
    output = f"{filename} {method}\n"
    output += f"{goal} {created}\n"
    output += " -> ".join(map(str, path))
    return output

# Command-line support
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python search.py <filename> <method>")
    else:
        result = run(sys.argv[1], sys.argv[2])
        print(result)
