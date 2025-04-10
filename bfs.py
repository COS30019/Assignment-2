import sys
from collections import deque

def parse_file(filename):
    nodes = {}
    edges = {}
    origin = None
    destinations = []

    with open(filename, 'r') as f:
        lines = f.readlines()
    
    mode = None
    for line in lines:
        line = line.strip()
        if line.startswith("Nodes:"):
            mode = "nodes"
        elif line.startswith("Edges:"):
            mode = "edges"
        elif line.startswith("Origin:"):
            mode = "origin"
        elif line.startswith("Destinations:"):
            mode = "destinations"
        elif mode == "nodes" and line:
            id_str, coord = line.split(":")
            nodes[int(id_str.strip())] = eval(coord.strip())
        elif mode == "edges" and line:
            edge_str, cost = line.split(":")
            from_to = eval(edge_str.strip())
            edges.setdefault(from_to[0], []).append((from_to[1], int(cost.strip())))
        elif mode == "origin":
            origin = int(line.strip())
        elif mode == "destinations":
            destinations = list(map(int, line.split(";")))

    return nodes, edges, origin, destinations

def bfs(nodes, edges, origin, destinations):
    frontier = deque([(origin, [origin])])
    explored = set()
    nodes_created = 1

    while frontier:
        current, path = frontier.popleft()
        if current in destinations:
            return current, nodes_created, path
        
        explored.add(current)

        for neighbor, _ in sorted(edges.get(current, [])):
            if neighbor not in explored and all(neighbor != n for n, _ in frontier):
                frontier.append((neighbor, path + [neighbor]))
                nodes_created += 1
    
    return None, nodes_created, []

def main():
    if len(sys.argv) != 3:
        print("Usage: python search.py <filename> <method>")
        return
    
    filename = sys.argv[1]
    method = sys.argv[2].upper()

    if method != "BFS":
        print(f"Method '{method}' not implemented in this file.")
        return

    nodes, edges, origin, destinations = parse_file(filename)
    goal, created, path = bfs(nodes, edges, origin, destinations)

    print(f"{filename} {method}")
    if goal is not None:
        print(f"{goal} {created}")
        print(" ".join(map(str, path)))
    else:
        print("No path found.")

if __name__ == "__main__":
    main()
